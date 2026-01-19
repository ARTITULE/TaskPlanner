import uuid
from task_planner.models.task import Task
from task_planner.services.task_service import TaskService


class TaskManager:
    def __init__(self):
        self.tasks: list[Task] = []
        self.service = TaskService()

    def add_task(self, title: str, description: str | None = None) -> Task:
        task = Task(
            id = str(uuid.uuid4()),
            title = title, 
            description = description
        )
        self.tasks.append(task)

        self.service.update_task(task=task)

        return task

    def delete_task(self, task_id: str):
        for task in self.tasks:
            if task.id == task_id:
                task.deleted = True
                self.service.update_task(task=task)
                break


    def set_completed(self, task_id: str, completed: bool):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = completed
                self.service.update_task(task=task)
                break
