from app.business_logic.exceptions import ResourceNotFound, ResourceAlreadyExists
from app.business_logic.models import Client, RedirectUri, ClientRedirectUriLink
from app.business_logic.repositories.resource_repository import ResourceRepository
from sqlmodel import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import Optional


class ClientRepository(ResourceRepository):
    def get_resources(self, limit: int, offset: int):
        with self.session as session:
            statement = select(Client).offset(offset).limit(limit)
            results = session.exec(statement)
            return results.all()

    def create_new_resource(self, resource: Client) -> Client:
        with self.session as session:
            session.add(resource)
            for redirect_uri in resource.redirect_urls:
                session.add(redirect_uri)
            try:
                session.commit()
            except IntegrityError as e:
                raise ResourceAlreadyExists(str(e))
            return None

    def find_resource(self, identifier: str) -> Optional[Client]:
        with self.session as session:
            statement = select(Client).where(Client.client_id == identifier)
            results = session.exec(statement)
            try:
                client = results.one()
            except NoResultFound:
                return None
            return client

    def delete_resource(self, identifier: str):
        with self.session as session:
            statement = select(Client).where(Client.client_id == identifier)
            results = session.exec(statement)
            try:
                resource = results.one()
            except NoResultFound:
                raise ResourceNotFound(identifier)
            session.delete(resource)
            session.commit()

    def get_client_by_identifiers(
            self,
            client_id: str,
            redirect_uri: Optional[str] = None,
            client_secret: Optional[str] = None
    ) -> Optional[Client]:
        with self.session as session:
            statement = select(Client).where(Client.client_id == client_id)
            if client_secret:
                statement = statement.where(Client.client_secret == client_secret)
            if redirect_uri:
                statement = statement \
                    .join(ClientRedirectUriLink).where(Client.client_id == ClientRedirectUriLink.client_id) \
                    .where(ClientRedirectUriLink.redirect_uri_id == redirect_uri)
            results = session.exec(statement)
            try:
                return results.one()
            except NoResultFound:
                return None
