from task_planner.models.task import Task

class TaskService:

    def update_task(self, task:Task) -> bool:

        payload = task.to_dict()

        print("sent task")
        print(payload)

        return True