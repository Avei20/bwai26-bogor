import os
import re
from datetime import datetime

class TaskStore:
    def __init__(self, filepath="tasks.md"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                f.write("# Tasks\n\n## Task List\n\n| ID | Title | Status | Priority | Created | Description |\n|----|-------|--------|----------|---------|-------------|\n")

    def _read_file(self) -> str:
        with open(self.filepath, "r") as f:
            return f.read()

    def _write_file(self, content: str):
        with open(self.filepath, "w") as f:
            f.write(content)

    def _parse_table(self, content: str) -> list[dict]:
        tasks = []
        lines = content.splitlines()
        table_start = -1
        for i, line in enumerate(lines):
            if line.strip().startswith("| ID |"):
                table_start = i
                break
        
        if table_start == -1 or table_start + 2 >= len(lines):
            return []

        header = [h.strip() for h in lines[table_start].split("|")[1:-1]]
        for line in lines[table_start + 2:]:
            if not line.strip().startswith("|"):
                break
            values = [v.strip() for v in line.split("|")[1:-1]]
            if len(values) == len(header):
                task = dict(zip(header, values))
                task["ID"] = int(task["ID"])
                tasks.append(task)
        return tasks

    def _render_table(self, tasks: list[dict]) -> str:
        header = "| ID | Title | Status | Priority | Created | Description |"
        separator = "|----|-------|--------|----------|---------|-------------|"
        rows = [header, separator]
        for t in sorted(tasks, key=lambda x: x["ID"]):
            rows.append(f"| {t['ID']} | {t['Title']} | {t['Status']} | {t['Priority']} | {t['Created']} | {t['Description']} |")
        
        content = self._read_file()
        lines = content.splitlines()
        table_start = -1
        for i, line in enumerate(lines):
            if line.strip().startswith("| ID |"):
                table_start = i
                break
        
        if table_start == -1:
            # Should not happen if _ensure_file_exists worked
            return content + "\n" + "\n".join(rows) + "\n"
        
        new_lines = lines[:table_start] + rows
        # Find if there is content after the table
        table_end = table_start + 2
        while table_end < len(lines) and lines[table_end].strip().startswith("|"):
            table_end += 1
        
        new_lines += lines[table_end:]
        return "\n".join(new_lines) + "\n"

    def get_all_tasks(self) -> list[dict]:
        content = self._read_file()
        return self._parse_table(content)

    def get_task(self, task_id: int) -> dict | None:
        tasks = self.get_all_tasks()
        for t in tasks:
            if t["ID"] == task_id:
                return t
        return None

    def add_task(self, title: str, description: str = "", priority: str = "medium") -> dict:
        tasks = self.get_all_tasks()
        next_id = max([t["ID"] for t in tasks], default=0) + 1
        new_task = {
            "ID": next_id,
            "Title": title,
            "Status": "pending",
            "Priority": priority,
            "Created": datetime.now().strftime("%Y-%m-%d"),
            "Description": description
        }
        tasks.append(new_task)
        self._write_file(self._render_table(tasks))
        return new_task

    def update_task(self, task_id: int, **fields) -> dict | None:
        tasks = self.get_all_tasks()
        updated_task = None
        for t in tasks:
            if t["ID"] == task_id:
                for key, value in fields.items():
                    if value and key in t:
                        t[key] = value
                updated_task = t
                break
        
        if updated_task:
            self._write_file(self._render_table(tasks))
        return updated_task

    def delete_task(self, task_id: int) -> bool:
        tasks = self.get_all_tasks()
        initial_len = len(tasks)
        tasks = [t for t in tasks if t["ID"] != task_id]
        if len(tasks) < initial_len:
            self._write_file(self._render_table(tasks))
            return True
        return False

# Singleton instance
store = TaskStore()
