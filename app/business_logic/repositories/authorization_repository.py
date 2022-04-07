from logging import Logger
from typing import Optional

from sqlmodel import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import select
from app.business_logic.exceptions import ResourceNotFound, AuthorizationCodeAlreadyExists
from app.business_logic.models import AuthorizationData


class AuthorizationRepository:
    def __init__(self, logger: Logger, session_factory):
        self.logger = logger
        self.session: Session = session_factory()

    def store_authorization_data(self, data: AuthorizationData):
        with self.session as session:
            session.add(data)
            try:
                session.commit()
            except IntegrityError as e:
                raise AuthorizationCodeAlreadyExists(str(e))

    def get_authorization_data(self, code: str) -> Optional[AuthorizationData]:
        with self.session as session:
            statement = select(AuthorizationData).where(AuthorizationData.code == code)
            results = session.exec(statement)
            try:
                auth_data = results.one()
            except NoResultFound:
                return None
            return auth_data

    def delete_authorization_data(self, code: str):
        with self.session as session:
            statement = select(AuthorizationData).where(AuthorizationData.code == code)
            results = session.exec(statement)
            try:
                resource = results.one()
            except NoResultFound:
                raise ResourceNotFound(code)
            session.delete(resource)
            session.commit()
