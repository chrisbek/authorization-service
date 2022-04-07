from urllib.parse import unquote

from pydantic import BaseModel, validator
from app.business_logic.exceptions import UnsupportedFlow
from app.business_logic.models import AuthorizationData


class CodeGrantDTO(BaseModel):
    grant_type: str
    code: str
    redirect_uri: str
    client_id: str
    client_secret: str

    @validator("grant_type", always=True)
    def check_str(cls, value):
        if value != 'authorization_code':
            raise UnsupportedFlow('Flow not supported')

    @validator('redirect_uri', always=True)
    def replace_hyphen(cls, v):
        return unquote(v)


class RefreshTokenGrantDTO(BaseModel):
    grant_type: str
    refresh_token: str
    client_id: str
    client_secret: str

    @validator("grant_type", always=True)
    def check_str(cls, value):
        if value != 'refresh_token':
            raise UnsupportedFlow('Flow not supported')


class PostTokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str

    @staticmethod
    def get_dto(auth_data: AuthorizationData):
        return PostTokenResponseDTO(
            access_token=auth_data.access_token,
            refresh_token=auth_data.refresh_token,
            id_token=auth_data.id_token,
        )
