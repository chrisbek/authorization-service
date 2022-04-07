from app.business_logic.models import User
from pydantic import BaseModel


class UserDTO(BaseModel):
    email: str
    password: str
    first_name: str

    def get_user_model(self) -> User:
        return User(
            email=self.email,
            password=self.password,
            first_name=self.first_name
        )

    @staticmethod
    def get_dto(user: User) -> 'UserDTO':
        return UserDTO(
            email=user.email,
            password=user.password,
            first_name=user.first_name
        )
