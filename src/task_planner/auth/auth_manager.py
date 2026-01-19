from task_planner.auth.user import User


class AuthManager:

    def __init__(self):
        self.current_user: User | None = None


    def login(self, username: str, password:str) -> User | None:
        if username and password:
            user = User(username=username, token="test_token")
            self.current_user = user
            return user
        
        return None
    
    def logout(self):
        self.current_user = None

    def is_authenticated(self) -> bool:
        return self.current_user is not None







