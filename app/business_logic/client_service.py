from typing import List
from app.business_logic.exceptions import ResourceNotFound
from app.business_logic.models import Client
from app.business_logic.repositories.resource_repository import ResourceRepository


class ClientService:
    def __init__(self, client_repo: ResourceRepository):
        self.client_repo = client_repo

    def get_clients(self, limit: int, offset: int) -> List[Client]:
        return self.client_repo.get_resources(limit=limit, offset=offset)

    def create_new_client(self, client: Client):
        """
        :raises ResourceAlreadyExists
        """
        self.client_repo.create_new_resource(client)

    def find_client(self, client_id: str) -> Client:
        """
        :raises ResourceNotFound
        """
        client = self.client_repo.find_resource(client_id)
        if not client:
            raise ResourceNotFound(f'Client {client_id} not found')

        return client

    def delete_client(self, client_id: str):
        """
        :raises ResourceNotFound
        :raises RepositoryGenericException
        """
        self.client_repo.delete_resource(client_id)
