class BusinessLogicException(Exception):
    pass


class ServerException(Exception):
    pass


class ResourceAlreadyExists(BusinessLogicException):
    pass


class AuthorizationCodeAlreadyExists(ServerException):
    pass


class ResourceNotFound(BusinessLogicException):
    pass


class RepositoryGenericException(ServerException):
    pass


class UnsupportedFlow(BusinessLogicException):
    pass


class InvalidRefreshToken(BusinessLogicException):
    pass


class InvalidRequest(BusinessLogicException):
    pass


class Unauthorized(BusinessLogicException):
    pass
