
from task_planner.models.task import Task


class TaskManager:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, title: str, description: str | None = None) -> Task:
        task = Task(title= title, description=description)
        self.tasks.append(task)
        return task

    def delete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)

    def set_completed(self, index: int, completed: bool):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = completed
