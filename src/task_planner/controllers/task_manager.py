import uuid
import json
from task_planner.models.task import Task
from task_planner.services.task_service import TaskService
from task_planner.services.local_task_service import LocalTaskService
from task_planner.auth.auth_manager import AuthManager
from task_planner.config import DATA_PATH
from datetime import date


class TaskManager:


    def __init__(self, auth_manager: AuthManager):
        self.tasks: list[Task] = []
        self.auth_manager = auth_manager

        self.remote_service = TaskService(auth_manager=auth_manager)
        self.local_service = LocalTaskService()

        self.data_path = DATA_PATH

    def add_task(self, title: str, description: str | None = None, category: str | None = None, exp_time = None) -> Task:
        task = Task(
            id = str(uuid.uuid4()),
            title = title, 
            description = description,
            exp_time = exp_time,
            category = category
        )
        self.tasks.append(task)

        service = self.get_service()
        service.create_task(task=task)

        return task

    def update_task(self, task_id: str, title: str, description: str, category: str, exp_time):
        for task in self.tasks:
            if task.id == task_id:
                task.title = title
                task.description = description
                task.category = category
                task.exp_time = exp_time
                service = self.get_service()
                service.update_task(task=task)
                break

    def delete_task(self, task_id: str):
        for task in self.tasks:
            if task.id == task_id:
                service = self.get_service()
                service.delete_task(task=task)
                break


    def set_completed(self, task_id: str, completed: bool):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = completed
                service = self.get_service()
                service.update_task(task=task)
                break

    def get_task(self, task_id: str):
        for task in self.tasks:
            if task.id == task_id:
                return task
            
    def get_service(self):
        if self.auth_manager.is_authenticated():
            return self.remote_service
        else:
            return self.local_service
        

    def load_tasks(self) -> list[Task]:

        if not self.data_path.exists():
            return []
        
        with self.data_path.open("r", encoding="utf-8") as f:
            raw_tasks = json.load(f)

        tasks: list[Task] = []

        for item in raw_tasks:
            task = Task(
                id= item["uuid"],
                title= item["title"],
                description= item.get("description"),
                exp_time= date.fromisoformat(item.get("exp_time")) if item.get("exp_time") else None,
                category= item.get("category"),
                completed= item.get("completed", False),
            )
            tasks.append(task)
        
        self.tasks = tasks
        return tasks