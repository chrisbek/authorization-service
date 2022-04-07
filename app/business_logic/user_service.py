from typing import List
from app.business_logic.exceptions import ResourceNotFound
from app.business_logic.models import User
from app.business_logic.repositories.resource_repository import ResourceRepository


class UserService:
    def __init__(self, user_repo: ResourceRepository):
        self.user_repo = user_repo

    def get_users(self, limit: int, offset: int) -> List[User]:
        return self.user_repo.get_resources(limit=limit, offset=offset)

    def create_new_user(self, user: User) -> User:
        """
        :raises ResourceAlreadyExists
        """
        return self.user_repo.create_new_resource(user)

    def find_user(self, email: str) -> User:
        """
        :raises ResourceNotFound
        """
        user = self.user_repo.find_resource(email)
        if not user:
            raise ResourceNotFound(f'User {email} not found')

        return user

    def delete_user(self, email: str):
        """
        :raises ResourceNotFound
        :raises RepositoryGenericException
        """
        self.user_repo.delete_resource(email)
