from app.business_logic.exceptions import ResourceNotFound, ResourceAlreadyExists
from app.business_logic.models import User
from app.business_logic.repositories.resource_repository import ResourceRepository
from sqlmodel import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import Optional


class UserRepository(ResourceRepository):
    def get_resources(self, limit: int, offset: int):
        with self.session as session:
            statement = select(User).offset(offset).limit(limit)
            results = session.exec(statement)
            return results.all()

    def create_new_resource(self, resource: User) -> User:
        with self.session as session:
            session.add(resource)
            try:
                session.commit()
            except IntegrityError as e:
                raise ResourceAlreadyExists(str(e))
            session.refresh(resource)
            return resource

    def find_resource(self, email: str) -> Optional[User]:
        with self.session as session:
            statement = select(User).where(User.email == email)
            results = session.exec(statement)
            try:
                return results.one()
            except NoResultFound:
                return None

    def get_user_by_external_identifier(self, external_id: str) -> Optional[User]:
        with self.session as session:
            statement = select(User).where(User.external_identifier == external_id)
            results = session.exec(statement)
            try:
                return results.one()
            except NoResultFound:
                return None

    def delete_resource(self, identifier: str):
        with self.session as session:
            statement = select(User).where(User.email == identifier)
            results = session.exec(statement)
            try:
                resource = results.one()
            except NoResultFound:
                raise ResourceNotFound(identifier)
            session.delete(resource)
            session.commit()

    def get_user(self, email, password):
        with self.session as session:
            statement = select(User).where(User.email == email).where(User.password == password)
            results = session.exec(statement)
            try:
                return results.one()
            except NoResultFound:
                return None
