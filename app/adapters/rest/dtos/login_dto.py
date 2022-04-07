from pydantic import BaseModel


class LoginDTO(BaseModel):
    email: str
    password: str
    client_id: str
    redirect_uri: str
    scope: str
    state: str


class LoginResponseDTO(BaseModel):
    code: str
    redirect_uri: str
    state: str
    client_id: str

