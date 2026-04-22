# Task Management Agent — Implementation Plan

## Overview
Build an AI-powered Task Management Assistant using Google ADK (Python), OpenRouter as AI provider,
with a single markdown file as the source of truth. The agent is exposed via the ADK Dev UI and
launched with `uv run main.py`.

---

## Phase 1: Project Setup & Dependencies

### Step 1.1 — Configure `pyproject.toml`
Update `pyproject.toml` with all required dependencies:
```toml
[project]
name = "serena"
version = "0.1.0"
description = "Task Management AI Agent using Google ADK"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "google-adk>=1.0.0",
    "litellm",
    "python-dotenv",
    "uvicorn",
]
```

### Step 1.2 — Create `.env` file
```env
OPENROUTER_API_KEY=<your-openrouter-api-key>
```

### Step 1.3 — Install dependencies
```bash
uv sync
```

---

## Phase 2: Task Storage Layer (Markdown File)

### Step 2.1 — Create `task_manager/task_store.py`
Implement a `TaskStore` class that reads/writes tasks to `tasks.md`.

**Markdown format for `tasks.md`:**
```markdown
# Tasks

## Task List

| ID | Title | Status | Priority | Created | Description |
|----|-------|--------|----------|---------|-------------|
| 1  | Buy groceries | pending | medium | 2026-04-22 | Buy milk, eggs, bread |
| 2  | Fix bug #123 | in_progress | high | 2026-04-22 | Null pointer in auth module |
```

**TaskStore class responsibilities:**
- `get_all_tasks() -> list[dict]` — Parse markdown table, return list of task dicts
- `add_task(title, description, priority) -> dict` — Append row, auto-increment ID
- `update_task(task_id, **fields) -> dict` — Update specific fields by ID
- `delete_task(task_id) -> bool` — Remove a task row by ID
- `get_task(task_id) -> dict | None` — Get single task by ID
- `_read_file() -> str` — Read the markdown file
- `_write_file(content: str)` — Write the markdown file
- `_parse_table(content: str) -> list[dict]` — Parse markdown table to dicts
- `_render_table(tasks: list[dict]) -> str` — Render dicts back to markdown table

**Valid statuses:** `pending`, `in_progress`, `done`, `cancelled`
**Valid priorities:** `low`, `medium`, `high`, `critical`

---

## Phase 3: Agent Tools (ADK Function Tools)

### Step 3.1 — Create `task_manager/tools.py`
Define plain Python functions that ADK will auto-wrap as tools.
Each function operates on the `TaskStore` singleton.

```python
# Tool functions to implement:

def list_tasks(status: str = "", priority: str = "") -> str:
    """List all tasks, optionally filtered by status or priority."""

def add_task(title: str, description: str = "", priority: str = "medium") -> str:
    """Add a new task with the given title, description, and priority."""

def update_task(task_id: int, title: str = "", description: str = "",
                status: str = "", priority: str = "") -> str:
    """Update an existing task's fields. Only non-empty fields are updated."""

def delete_task(task_id: int) -> str:
    """Delete a task by its ID."""

def get_task(task_id: int) -> str:
    """Get detailed information about a specific task."""

def complete_task(task_id: int) -> str:
    """Mark a task as done."""
```

**Key design decisions:**
- Tools return **strings** (not dicts) so the LLM can directly use them in responses
- The `TaskStore` is instantiated as a module-level singleton
- Each tool function has a clear docstring (ADK uses these for the LLM's tool schema)
- No `ToolContext` needed — tools operate directly on the file system

---

## Phase 4: Agent Definition

### Step 4.1 — Create `task_manager/__init__.py`
This file is required by ADK's agent directory convention. It must export `root_agent`.

```python
from .agent import root_agent
```

### Step 4.2 — Create `task_manager/agent.py`
Define the root agent using ADK's `Agent` class with `LiteLlm` wrapper.

```python
from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools import list_tasks, add_task, update_task, delete_task, get_task, complete_task

root_agent = Agent(
    name="task_manager",
    model=LiteLlm(model="openrouter/openrouter/auto"),
    instruction="""You are a Task Management Assistant. You help users manage their tasks
    using the available tools.

    When users want to:
    - See tasks: use list_tasks (can filter by status/priority)
    - Add a task: use add_task
    - Update a task: use update_task
    - Delete a task: use delete_task
    - View a task: use get_task
    - Mark complete: use complete_task

    Always confirm actions and show the updated task list after modifications.
    Format responses clearly with task details.
    Be proactive — suggest next actions when appropriate.""",
    description="Manages tasks stored in a markdown file",
    tools=[list_tasks, add_task, update_task, delete_task, get_task, complete_task],
)
```

**Model note:** `openrouter/openrouter/auto` routes through OpenRouter's free model tier.
Alternative free models: `openrouter/google/gemma-3-1b-it:free`, `openrouter/meta-llama/llama-4-scout:free`.

---

## Phase 5: Main Entry Point with Dev UI

### Step 5.1 — Create `main.py`
The entry point uses `google.adk.cli.fast_api.get_fast_api_app` to create the FastAPI app
and serves it with `uvicorn`, which includes the built-in ADK Dev UI.

```python
import os
import uvicorn
from dotenv import load_dotenv
from google.adk.cli.fast_api import get_fast_api_app

load_dotenv()

# Create the FastAPI app pointing to the directory containing agent packages
app = get_fast_api_app(
    agent_dir=".",           # Current dir contains task_manager/ package
    web=True,                # Enable Dev UI
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Dev UI Access:** After running `uv run main.py`, open `http://127.0.0.1:8001/dev-ui/`

---

## Phase 6: Initialize Task File

### Step 6.1 — Create initial `tasks.md`
```markdown
# Tasks

## Task List

| ID | Title | Status | Priority | Created | Description |
|----|-------|--------|----------|---------|-------------|
```

---

## Final Project Structure
```
serena/
├── .env                      # API keys (OPENROUTER_API_KEY)
├── .python-version           # Python 3.14
├── .serena/                  # Serena config
├── AGENT.md                  # Agent instructions for Serena
├── PROMPT.md                 # Original requirements
├── README.md                 # Documentation
├── main.py                   # Entry point: uv run main.py
├── pyproject.toml            # Dependencies (uv)
├── tasks.md                  # Single source of truth for tasks
└── task_manager/             # ADK agent package
    ├── __init__.py           # Exports root_agent
    ├── agent.py              # Agent definition (LiteLlm + OpenRouter)
    ├── tools.py              # Task CRUD tool functions
    └── task_store.py         # Markdown file parser/writer
```

---

## Implementation Order (Step-by-Step)

| Step | File | Description |
|------|------|-------------|
| 1 | `pyproject.toml` | Add dependencies |
| 2 | `.env` | Add OpenRouter API key |
| 3 | `uv sync` | Install deps |
| 4 | `tasks.md` | Create initial empty task file |
| 5 | `task_manager/task_store.py` | Implement markdown CRUD logic |
| 6 | `task_manager/tools.py` | Implement ADK tool functions |
| 7 | `task_manager/__init__.py` | Export `root_agent` |
| 8 | `task_manager/agent.py` | Define agent with LiteLlm + tools |
| 9 | `main.py` | FastAPI + Dev UI entry point |
| 10 | `uv run main.py` | Test & verify |

---

## Verification Checklist
- [ ] `uv sync` installs all dependencies without errors
- [ ] `uv run main.py` starts the server on port 8001
- [ ] Dev UI accessible at `http://127.0.0.1:8001/dev-ui/`
- [ ] `task_manager` agent appears in the Dev UI app selector
- [ ] Can add a task via natural language ("Add a task to buy groceries")
- [ ] Can list tasks ("Show me all tasks")
- [ ] Can update a task ("Change task 1 priority to high")
- [ ] Can complete a task ("Mark task 1 as done")
- [ ] Can delete a task ("Delete task 1")
- [ ] `tasks.md` file is updated after each operation
- [ ] Agent responds conversationally with clear formatting
