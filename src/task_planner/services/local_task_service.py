import json
from task_planner.models.task import Task
from task_planner.config import DATA_PATH


class LocalTaskService:
    def __init__(self):

        self.path = DATA_PATH

        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True)

        if not self.path.exists():
            self.path.write_text("[]")

    def _load(self) -> list[dict]:
        return json.loads(self.path.read_text())

    def _save(self, data: list[dict]):
        self.path.write_text(json.dumps(data, indent=2))

    def create_task(self, task: Task):
        tasks = self._load()
        tasks.append(task.to_dict())
        self._save(tasks)

    def update_task(self, task: Task):
        tasks = self._load()
        for t in tasks:
            if t["uuid"] == task.id:
                t.update(task.to_dict())
                break
        self._save(tasks)

    def delete_task(self, task: Task):
        tasks = self._load()
        tasks = [t for t in tasks if t["uuid"] != task.id]
        self._save(tasks)
