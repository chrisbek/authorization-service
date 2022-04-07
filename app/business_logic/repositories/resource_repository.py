from abc import ABC, abstractmethod
from sqlmodel import Session
from logging import Logger
from typing import Any, Optional


class ResourceRepository(ABC):
    def __init__(self, logger: Logger, session_factory):
        self.logger = logger
        self.session: Session = session_factory()

    @abstractmethod
    def get_resources(self, limit: int, offset: int):
        raise NotImplementedError

    @abstractmethod
    def create_new_resource(self, resource: object) -> Any:
        """
        :raises ResourceAlreadyExists
        """
        raise NotImplementedError

    @abstractmethod
    def find_resource(self, identifier: Any) -> Optional[Any]:
        raise NotImplementedError

    @abstractmethod
    def delete_resource(self, identifier: Any):
        """
        :raises ResourceNotFound
        """
        raise NotImplementedError
