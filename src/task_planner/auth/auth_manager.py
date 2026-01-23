from task_planner.auth.user import User
import requests
from requests.exceptions import RequestException


class AuthManager:

    Base_URL = "https://introspectional-scalelike-ria.ngrok-free.dev"

    def __init__(self):
        self.current_user: User | None = None


    def login(self, email: str, password:str) -> User | None:
        payload = {
            "name": email,
            "password": password
        }
        print(payload)
        try:
            response = requests.post(
                f"{self.Base_URL}/login",
                json=payload,
                timeout=5,
            )
        except RequestException:
            print("1")
            return None
        
        if response.status_code != 200:
            return None
        
        data = response.json()

        user = User(
            username= data["name"],
            token= data["access_token"]
        )
        
        self.current_user = user
        return user

    def signup(self, name: str, surname: str, email: str, password: str) -> None:
        payload = {
            "name": name,
            "surname": surname,
            "email": email,
            "password": password,
        }
        print(payload)
        try:
            response = requests.post(
                f"{self.Base_URL}/sign_up",
                json=payload,
                timeout=5,
            )
        except RequestException:
            print("2")
            return None
        
        return response.status_code == 201

    
    def logout(self):
        self.current_user = None

    def is_authenticated(self) -> bool:
        return self.current_user is not None
    
    def get_current_user(self) -> User | None:
        return self.current_user

    def get_token(self) -> str | None:
        if self.current_user is None:
            return None
        return self.current_user.token







