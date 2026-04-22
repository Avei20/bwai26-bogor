from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools import list_tasks, add_task, update_task, delete_task, get_task, complete_task

root_agent = Agent(
    name="task_manager",
    model=LiteLlm(model="openrouter/openrouter/free"),
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
