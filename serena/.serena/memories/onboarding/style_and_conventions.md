# Style and Conventions

## Python
- Python 3.14+ (as defined in `.python-version` and `pyproject.toml`)
- Use type hints for all function signatures
- Use docstrings (Google-style) for all public functions and classes
- Use `snake_case` for functions/variables, `PascalCase` for classes
- Prefer async functions for tool implementations (ADK convention)

## ADK Conventions
- Agent definitions use `Agent()` constructor with `name`, `model`, `instruction`, `tools`
- Tools are plain Python functions with docstrings (auto-wrapped by ADK)
- Use `ToolContext` parameter for session state access
- Use `LiteLlm` wrapper for non-Gemini models
- Agent directory structure: `task_manager/__init__.py` + `agent.py`

## Task Completion Checklist
- Ensure `uv run main.py` starts without errors
- Verify the ADK Dev UI loads at the expected URL
- Test agent tools manually via the Dev UI
