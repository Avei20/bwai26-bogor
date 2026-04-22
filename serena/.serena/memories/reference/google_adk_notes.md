# Google ADK Reference Notes

## Dev UI Setup
The ADK Dev UI is a built-in web interface for interacting with agents during development.

### Two ways to launch:
1. **CLI**: `adk web path/to/agents_dir` — starts on `http://127.0.0.1:8080`
2. **Programmatic (preferred for this project)**:
   ```python
   from google.adk.cli.fast_api import get_fast_api_app
   app = get_fast_api_app(agent_dir=".", web=True)
   # Serve with uvicorn
   ```
   This creates a FastAPI app with endpoints: `/list-apps`, `/run_sse`, and serves the Dev UI at `/dev-ui/`.

### Agent Directory Convention
ADK discovers agents from a **directory** structure. Each agent is a Python package:
```
agent_dir/
└── task_manager/       # Package name = agent name
    ├── __init__.py     # Must export `root_agent`
    └── agent.py        # Agent definition
```

## LiteLLM Integration for OpenRouter
ADK uses `LiteLlm` wrapper to support non-Gemini models:
```python
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(model="openrouter/openrouter/auto")
```

### Required Environment Variables
- `OPENROUTER_API_KEY` — Your OpenRouter API key
- LiteLLM automatically reads this based on the `openrouter/` prefix

### Free Model Options on OpenRouter
- `openrouter/openrouter/auto` — Auto-routes to best free model
- `openrouter/google/gemma-3-1b-it:free`
- `openrouter/meta-llama/llama-4-scout:free`
- `openrouter/mistralai/mistral-small-3.1-24b-instruct:free`

## ADK Agent Constructor
```python
Agent(
    name="agent_name",          # Required: unique identifier
    model=LiteLlm(...),         # Required: model wrapper
    instruction="...",          # System prompt
    description="...",          # Short description
    tools=[func1, func2],      # List of tool functions
    output_key="key",          # Optional: store output in session state
    output_schema=Model,       # Optional: enforce structured output
)
```

## Tool Functions
Plain Python functions are auto-wrapped by ADK:
- Must have docstrings (used for LLM tool schema)
- Must have type hints on parameters
- Return strings for best LLM compatibility
- Use `ToolContext` parameter for session state access (injected by ADK)

## Runner
```python
from google.adk.runners import InMemoryRunner
runner = InMemoryRunner(agent=agent, app_name="my_app")
```
