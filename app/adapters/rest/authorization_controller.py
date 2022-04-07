from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from app.adapters.rest.dtos.code_grant_dto import PostTokenResponseDTO, CodeGrantDTO, RefreshTokenGrantDTO
from app.adapters.rest.dtos.login_dto import LoginDTO, LoginResponseDTO
from app.business_logic.exceptions import InvalidRequest, ResourceNotFound, Unauthorized
from app.business_logic.models import WellKnownData
from app.config.config import Container
from app.adapters.rest.serializer import Serializer

router = APIRouter()
authorization_service = Container.authorization_service()


@router.get("/.well-known/openid-configuration", response_model=WellKnownData)
def get_well_known_data() -> WellKnownData:
    return authorization_service.get_well_known_data()


@router.get("")
def redirect_to_home_with_data_in_cookie(client_id: str, scope: str, redirect_uri: str, state: str):
    Container.logger.error("fake_authorization_grant_endpoint invoked")
    Container.logger.warn(f'Yoooooooooooooooooooooooooooo {state}')

    response = RedirectResponse(f'{Container.base_url}', 302)
    Serializer.add_data_to_response_as_cookie(response, client_id, scope, redirect_uri, state)
    return response


@router.post("/login", response_model=LoginResponseDTO)
def login(login_dto: LoginDTO):
    """
    :raises ResourceNotFound
    :raises AuthorizationCodeAlreadyExists
    """
    try:
        # client = authorization_service.get_client(client_id=login_dto.client_id, redirect_uri=login_dto.redirect_uri)
        user = authorization_service.get_user(user_identifier=login_dto.email, password=login_dto.password)
    except ResourceNotFound as e:
        raise Unauthorized()
    code = authorization_service.generate_code(user)

    # # When you want to redirect to a GET after a POST, the best practice is to redirect with a 303 status code
    # return RedirectResponse(url=f'{login_dto.redirect_uri}?code={code}&state={login_dto.state}', status_code=303)

    return LoginResponseDTO(
        code=code, redirect_uri=login_dto.redirect_uri, state=login_dto.state, client_id=login_dto.client_id)


@router.post('/token', response_model=PostTokenResponseDTO)
async def get_token_code_grant(request: Request):
    """
    :raises ResourceNotFound
    """
    if 'content-type' not in request.headers:
        raise InvalidRequest('Content-type not specified')
    if request.headers['content-type'] != 'application/x-www-form-urlencoded':
        raise InvalidRequest('Content-type not supported')

    request_data = {}
    for item in (await request.body()).decode('utf-8').split('&'):
        key, value = item.split('=')
        request_data[key] = value

    if request_data['grant_type'] == 'authorization_code':
        data = CodeGrantDTO(**request_data)
    if request_data['grant_type'] == 'refresh_token':
        data = RefreshTokenGrantDTO(**request_data)

    if isinstance(data, CodeGrantDTO):
        # authorization_service.get_client(
        #     client_id=data.client_id, client_secret=data.client_secret, redirect_uri=data.redirect_uri)
        auth_data = authorization_service.get_authorization_data_from_code(data.code)
        authorization_service.remove_code(data.code)
        return PostTokenResponseDTO.get_dto(auth_data)

    if isinstance(data, RefreshTokenGrantDTO):
        # authorization_service.get_client(client_id=data.client_id, client_secret=data.client_secret)
        auth_data = authorization_service.refresh_token(data.refresh_token)
        return PostTokenResponseDTO.get_dto(auth_data)
