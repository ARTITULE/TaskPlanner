from task_planner.models.task import Task
from task_planner.auth.auth_manager import AuthManager
import requests
from requests.exceptions import RequestException

class TaskService:

    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager
        self.Base_URL = "https://introspectional-scalelike-ria.ngrok-free.dev"
        self.user = self.auth_manager.get_current_user()
    
    def create_task(self, task:Task) -> bool:

        if not self.user or not self.user.token:
            print("error, no user token")

        payload = task.to_dict()

        headers = {
            "Authorization": f"Bearer {1}",
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

        print("sent task create")

        if response.status_code != 200:
            return None
        else:
            return True
        


        
    def delete_task(self, task:Task) -> bool:

        if not self.user or not self.user.token:
            print("error, no user token")

        payload = {
            "uuid": task.id
        }


        headers = {
            "Authorization": f"Bearer {self.user.token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                f"{self.Base_URL}/task/delete",
                json=payload,
                headers=headers,
                timeout=5,
            )

        except RequestException:

            return None


    def update_task(self, task:Task) -> bool:

        if not self.user or not self.user.token:
            print("error, no user token")

        payload = task.to_dict()

        headers = {
            "Authorization": f"Bearer {1}",
            "Content-Type": "application/json",
        }
        print(headers)           
        print(payload)

        try:
            response = requests.post(
                f"{self.Base_URL}/task/update",
                json=payload,
                headers=headers,
                timeout=5,
            )
        except RequestException:
            print("3")
            return None
        
        try:
            self.verify(response.json())
            print("Got the ok response")
        
        except RequestException:
            print("there is a problem")

        print("sent task update")

        if response.status_code != 200:
            return None
        else:
            return True
        

    def verify(self, json) -> bool:

        response = json["message"]

        match response:

            case "ok":
                print(f"The response is ok ! {response}")
                return True
            
            case _:
                print(f"There is a problem with {response}")
                return False
