from task_planner.models.task import Task
from task_planner.auth.auth_manager import AuthManager
import requests
from requests.exceptions import RequestException

class TaskService:

    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager
        self.Base_URL = "https://introspectional-scalelike-ria.ngrok-free.dev"
    
    def update_task(self, task:Task) -> bool:

        user = self.auth_manager.get_current_user()
        if not user or not user.token:
            print("error, no user token")

        payload = task.to_dict()

        headers = {
            "Authorization": f"Bearer {user.token}",
            "Content-Type": "application/json",
        }
        print(headers)           
        print(payload)

        try:
            response = requests.post(
                f"{self.Base_URL}/task/create",
                json=payload,
                headers=headers,
                timeout=5,
            )
        except RequestException:
            print("3")
            return None
        
        
        #data = response.json()
        #print(data)

        print("sent task")

        if response.status_code != 200:
            return None
        else:
            return True
        
    