from .task_store import store

def list_tasks(status: str = "", priority: str = "") -> str:
    """List all tasks, optionally filtered by status or priority."""
    tasks = store.get_all_tasks()
    if status:
        tasks = [t for t in tasks if t["Status"].lower() == status.lower()]
    if priority:
        tasks = [t for t in tasks if t["Priority"].lower() == priority.lower()]
    
    if not tasks:
        return "No tasks found."
    
    res = "Current Tasks:\n"
    for t in tasks:
        res += f"- [{t['ID']}] {t['Title']} ({t['Status']}, {t['Priority']})\n"
    return res

def add_task(title: str, description: str = "", priority: str = "medium") -> str:
    """Add a new task with the given title, description, and priority."""
    task = store.add_task(title, description, priority)
    return f"Task added successfully: [{task['ID']}] {task['Title']}"

def update_task(task_id: int, title: str = "", description: str = "",
                status: str = "", priority: str = "") -> str:
    """Update an existing task's fields. Only non-empty fields are updated."""
    fields = {}
    if title: fields["Title"] = title
    if description: fields["Description"] = description
    if status: fields["Status"] = status
    if priority: fields["Priority"] = priority
    
    task = store.update_task(task_id, **fields)
    if task:
        return f"Task {task_id} updated successfully."
    return f"Task {task_id} not found."

def delete_task(task_id: int) -> str:
    """Delete a task by its ID."""
    if store.delete_task(task_id):
        return f"Task {task_id} deleted successfully."
    return f"Task {task_id} not found."

def get_task(task_id: int) -> str:
    """Get detailed information about a specific task."""
    task = store.get_task(task_id)
    if task:
        res = f"Task Details for [{task_id}]:\n"
        res += f"Title: {task['Title']}\n"
        res += f"Status: {task['Status']}\n"
        res += f"Priority: {task['Priority']}\n"
        res += f"Created: {task['Created']}\n"
        res += f"Description: {task['Description']}\n"
        return res
    return f"Task {task_id} not found."

def complete_task(task_id: int) -> str:
    """Mark a task as done."""
    task = store.update_task(task_id, Status="done")
    if task:
        return f"Task {task_id} marked as done."
    return f"Task {task_id} not found."
