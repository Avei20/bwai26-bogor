# Project Overview

## Purpose
This project is a **Task Management AI Agent** built using **Google Agent Development Kit (ADK)** for Python.
The agent helps users manage tasks (add, list, update, delete, mark complete) through natural language conversations,
with all tasks persisted in a single markdown file as the source of truth.

## Tech Stack
- **Language**: Python 3.14+
- **AI Framework**: Google ADK (Agent Development Kit) for Python
- **AI Provider**: OpenRouter (via LiteLLM integration)
- **Default Model**: `openrouter/openrouter/auto` (free tier models)
- **Package Manager**: `uv`
- **UI**: Google ADK built-in Dev UI (`adk web`)
- **Storage**: Single markdown file (`tasks.md`)
- **Entry Point**: `uv run main.py`

## Project Structure
```
serena/
├── .python-version       # Python version pin
├── .serena/              # Serena configuration
├── AGENT.md              # Agent instructions
├── PROMPT.md             # Project prompt/requirements
├── README.md             # Project readme
├── main.py               # Entry point
└── pyproject.toml        # Project configuration (uv)
```

## System
- **OS**: macOS (Darwin)
- **Shell**: zsh
