from app.business_logic.models import Client, RedirectUri
from pydantic import BaseModel
from typing import List


class ClientInputDTO(BaseModel):
    client_name: str
    redirect_urls: List[str]

    def get_client_model(self) -> Client:
        client = Client(client_name=self.client_name)
        for redirect_uri in self.redirect_urls:
            client.redirect_urls.append(RedirectUri(redirect_uri=redirect_uri))

        return client


class ClientOutDTO(BaseModel):
    client_name: str
    client_id: str

    @staticmethod
    def get_dto(client: Client) -> 'ClientOutDTO':
        return ClientOutDTO(
            client_name=client.client_name,
            client_id=client.client_id
        )


class ClientExtendedDTO(ClientInputDTO):
    client_id: str
    client_secret: str

    @staticmethod
    def get_dto(client: Client) -> 'ClientExtendedDTO':
        return ClientExtendedDTO(
            client_name=client.client_name,
            client_id=client.client_id,
            client_secret=client.client_secret,
            redirect_urls=[ru.redirect_uri for ru in client.redirect_urls]
        )
