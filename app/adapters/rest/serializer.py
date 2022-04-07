import jwt

from app.business_logic.authorizatiaon_service import AuthorizationService
from app.config.config import Container
from starlette.responses import Response


class Serializer:
    @staticmethod
    def add_data_to_response_as_cookie(response: Response, client_id: str, scope: str, redirect_uri: str, state: str):
        token = jwt.encode(
            {
                'redirect_uri': redirect_uri,
                'client_id': client_id,
                'state': state,
                'scope': scope,
            },
            Container.private_key,
            algorithm=AuthorizationService.AUTHORIZATION_ALGO
        )
        response.set_cookie(
            key='authorization_info',
            path='/',
            value=token,
            secure=True,
            samesite='strict'
        )
