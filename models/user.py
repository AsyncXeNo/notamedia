from enum import Enum


class UserType(Enum):
    SUPER_ADMIN = 1
    WORKER = 2
    CLIENT = 3

    def get_str(user_type: int):
        if user_type == UserType.SUPER_ADMIN.value:
            return "Super Admin"
        if user_type == UserType.WORKER.value:
            return "Worker"
        if user_type == UserType.CLIENT.value:
            return "Client"


class User:
    def __init__(self, name: str, hashed_password: str, user_type: int, active: bool = True):
        self.name = name
        self.hashed_password = hashed_password
        self.user_type = user_type
        self.active = active
    
    def to_dict(self):
        return {
            "name": self.name,
            "hashed_password": self.hashed_password,
            "user_type": self.user_type,
            "active": self.active
        }
