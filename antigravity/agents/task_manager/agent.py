import os
from pathlib import Path
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.models import LiteLlm

# Load environment variables
load_dotenv()

TASKS_FILE = Path("tasks.md")

def _ensure_tasks_file():
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("# Task List\n\n", encoding="utf-8")

def add_task(task_description: str) -> str:
    """Add a new task to the task list."""
    _ensure_tasks_file()
    with TASKS_FILE.open("a", encoding="utf-8") as f:
        f.write(f"- [ ] {task_description}\n")
    return f"Successfully added task: {task_description}"

def list_tasks() -> str:
    """List all tasks currently in the task list."""
    _ensure_tasks_file()
    content = TASKS_FILE.read_text(encoding="utf-8")
    return content if content.strip() else "The task list is currently empty."

def update_task(task_description: str, completed: bool) -> str:
    """Update a task's status (completed or not completed) by providing its exact description or a unique substring."""
    _ensure_tasks_file()
    lines = TASKS_FILE.read_text(encoding="utf-8").splitlines()
    updated = False
    
    for i, line in enumerate(lines):
        if line.startswith("- [") and task_description.lower() in line.lower():
            status_box = "[x]" if completed else "[ ]"
            # Extract the actual task text after the checkbox
            task_text = line[6:].strip() if len(line) >= 6 else line
            lines[i] = f"- {status_box} {task_text}"
            updated = True
            break
            
    if updated:
        TASKS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
        status_str = "completed" if completed else "not completed"
        return f"Successfully updated task '{task_description}' to {status_str}."
    else:
        return f"Could not find task matching: {task_description}"

def delete_task(task_description: str) -> str:
    """Delete a task from the list by providing its exact description or a unique substring."""
    _ensure_tasks_file()
    lines = TASKS_FILE.read_text(encoding="utf-8").splitlines()
    new_lines = []
    deleted = False
    
    for line in lines:
        if not deleted and line.startswith("- [") and task_description.lower() in line.lower():
            deleted = True
            continue # Skip this line to delete it
        new_lines.append(line)
            
    if deleted:
        TASKS_FILE.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return f"Successfully deleted task matching: {task_description}"
    else:
        return f"Could not find task matching: {task_description}"

# Define the root agent
root_agent = Agent(
    name="task_manager",
    description="An AI Assistant that manages a task list in a markdown file.",
    instruction=(
        "You are a helpful Task Management Assistant. "
        "You manage a single source of truth for tasks stored in a markdown file. "
        "Use the provided tools to add, list, update, and delete tasks based on user requests. "
        "Always communicate clearly what changes you have made."
    ),
    model=LiteLlm(model="openrouter/openrouter/free"),
    tools=[add_task, list_tasks, update_task, delete_task],
)
