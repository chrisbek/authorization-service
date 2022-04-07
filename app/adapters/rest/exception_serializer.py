from starlette.responses import JSONResponse
from app.adapters.rest.dtos.exceptions import get_error_code_for_exception
from fastapi import FastAPI, Request
from pydantic import ValidationError
from app.business_logic.exceptions import BusinessLogicException, ServerException, ResourceNotFound, Unauthorized


def get_json_response_for_exception(exc: Exception, status_code: int):
    return JSONResponse(
        {'message': str(exc), 'error_code': get_error_code_for_exception(exc)}, status_code=status_code)


async def _business_logic_exception_handler(request, exc):
    return get_json_response_for_exception(exc, status_code=409)


async def _server_exception_handler(request: Request, exc):
    return get_json_response_for_exception(exc, status_code=500)


async def _request_validation_error_handler(request: Request, exc):
    return get_json_response_for_exception(exc, status_code=400)


async def _resource_not_found_handler(request: Request, exc):
    return get_json_response_for_exception(exc, status_code=404)


async def _unauthorized(request: Request, exc):
    return get_json_response_for_exception(exc, status_code=401)


def add_exception_handlers_to_app(app: FastAPI):
    app.add_exception_handler(BusinessLogicException, _business_logic_exception_handler)
    app.add_exception_handler(ServerException, _server_exception_handler)
    app.add_exception_handler(ValidationError, _request_validation_error_handler)
    app.add_exception_handler(ResourceNotFound, _resource_not_found_handler)
    app.add_exception_handler(Unauthorized, _unauthorized)
