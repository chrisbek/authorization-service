import logging
from logging import Logger, getLogger
from dependency_injector import containers, providers

from app.business_logic.repositories.authorization_repository import AuthorizationRepository
from app.business_logic.repositories.client_repository import ClientRepository
from app.business_logic.repositories.user_repository import UserRepository
from app.business_logic.authorizatiaon_service import AuthorizationService
from app.business_logic.client_service import ClientService
from app.business_logic.user_service import UserService
from app.config.database import DatabaseFactory


def get_logger(log_level: str) -> Logger:
    logger = getLogger()
    logger.setLevel(log_level)
    return logger


def get_client_repository(logger, session_factory):
    return providers.Singleton(
        ClientRepository,
        logger,
        session_factory
    )


def get_user_repository(logger, session_factory):
    return providers.Singleton(
        UserRepository,
        logger,
        session_factory
    )


def get_auth_repository(logger, session_factory):
    return providers.Singleton(
        AuthorizationRepository,
        logger,
        session_factory
    )


def get_client_service(client_repository):
    return providers.Singleton(
        ClientService,
        client_repo=client_repository
    )


def get_user_service(user_repository):
    return providers.Singleton(
        UserService,
        user_repo=user_repository
    )


def get_authorization_service(
        client_repository, user_repository, auth_repository, public_key, private_key, token_endpoint):
    return providers.Singleton(
        AuthorizationService,
        client_repository,
        user_repository,
        auth_repository,
        public_key,
        private_key,
        token_endpoint
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.platform_name.from_env("PLATFORM", as_=str, required=True)
    config.private_key.from_env("PRIVATE_KEY", as_=str, required=True)
    config.public_key.from_env("PUBLIC_KEY", as_=str, required=True)
    config.log_level.from_env("LOG_LEVEL", default=logging.ERROR)
    config.base_url.from_env("BASE_URL", as_=str, required=True)

    platform_name = config.platform_name()
    private_key = config.private_key()
    public_key = config.public_key()
    log_level = config.log_level()
    base_url = config.base_url()

    logger = get_logger(log_level)
    client_repository = get_client_repository(logger, DatabaseFactory.get_session)
    user_repository = get_user_repository(logger, DatabaseFactory.get_session)
    auth_repository = get_auth_repository(logger, DatabaseFactory.get_session)
    client_service = get_client_service(client_repository)
    user_service = get_user_service(user_repository)
    authorization_service = get_authorization_service(
        client_repository, user_repository, auth_repository, public_key, private_key,
        token_endpoint=f'{base_url}/auth/token')
