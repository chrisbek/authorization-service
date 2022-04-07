import json
from typing import Tuple, Optional
from uuid import uuid4
from rsa import DecryptionError
from app.business_logic.exceptions import ResourceNotFound, InvalidRefreshToken
from app.business_logic.repositories.authorization_repository import AuthorizationRepository
from app.business_logic.models import Client, User, AuthorizationData, WellKnownData
from app.business_logic.repositories.client_repository import ClientRepository
from app.business_logic.repositories.user_repository import UserRepository
import jwt
import rsa


class AuthorizationService:
    AUTHORIZATION_ALGO = 'RS512'

    def __init__(
            self,
            client_repository: ClientRepository,
            user_repository: UserRepository,
            auth_repository: AuthorizationRepository,
            public_key: str,
            private_key: str,
            token_endpoint: str
    ):
        self.client_repository = client_repository
        self.user_repository = user_repository
        self.auth_repository = auth_repository
        self.public_key = public_key
        self.private_key = private_key
        self.token_endpoint = token_endpoint

    def get_client(
            self,
            client_id: str,
            redirect_uri: Optional[str] = None,
            client_secret: Optional[str] = None
    ) -> Client:
        """
        :raises ResourceNotFound
        """
        client = self.client_repository.get_client_by_identifiers(
            client_id=client_id, redirect_uri=redirect_uri, client_secret=client_secret)
        if not client:
            raise ResourceNotFound(f'Client not found {client_id, redirect_uri}')

        return client

    def get_user(self, user_identifier: str, password: str) -> User:
        """
        :raises ResourceNotFound
        """
        user = self.user_repository.get_user(user_identifier, password)
        if not user:
            raise ResourceNotFound()
        return user

    def generate_code(self, user: User) -> str:
        """
        :raises AuthorizationCodeAlreadyExists
        """
        access_token, refresh_token, id_token = self._generate_tokens(user)
        code = str(uuid4())
        auth_data = AuthorizationData(
            code=code,
            access_token=access_token,
            refresh_token=refresh_token,
            id_token=id_token
        )
        self.auth_repository.store_authorization_data(auth_data)
        return code

    def get_authorization_data_from_code(self, code: str) -> AuthorizationData:
        """
        :raises ResourceNotFound
        """
        auth_data = self.auth_repository.get_authorization_data(code)
        if not auth_data:
            raise ResourceNotFound(code)
        return auth_data

    def remove_code(self, code: str):
        """
        :raises ResourceNotFound
        """
        self.auth_repository.delete_authorization_data(code)

    def refresh_token(self, refresh_token_jwt_encrypted: str) -> AuthorizationData:
        """
        :raises InvalidRefreshToken
        """
        refresh_token_dict = jwt.decode(
            refresh_token_jwt_encrypted,
            self.private_key,
            algorithms=[self.AUTHORIZATION_ALGO],
            options={
                "verify_signature": False
            })  # TODO: verify_signature: False is required due to some bug in frontend
        enc_string = refresh_token_dict['value']
        enc_bytes = bytes.fromhex(enc_string)
        rsa_private_key = rsa.PrivateKey.load_pkcs1(self.private_key)
        try:
            decrypted_str = rsa.decrypt(enc_bytes, rsa_private_key).decode()
        except DecryptionError:
            raise InvalidRefreshToken()
        decrypted_dict = json.loads(decrypted_str)
        user_external_identifier = decrypted_dict['sub']

        user = self.user_repository.get_user_by_external_identifier(user_external_identifier)
        if not user:
            raise InvalidRefreshToken()

        access_token, refresh_token, id_token = self._generate_tokens(user)
        return AuthorizationData(
            code='dummy',
            access_token=access_token,
            refresh_token=refresh_token,
            id_token=id_token
        )

    def get_well_known_data(self) -> WellKnownData:
        return WellKnownData(
            public_key=self.public_key,
            token_endpoint=self.token_endpoint
        )

    def _generate_tokens(self, user: User) -> Tuple:
        """
        A refresh token must not allow the client to gain any access beyond the scope of the original grant.
        The refresh token exists to enable authorization servers to use short lifetimes for access tokens without
        needing to involve the user when the token expires.
        """
        access_token = jwt.encode({
            'sub': user.external_identifier,
        }, self.private_key, self.AUTHORIZATION_ALGO)
        id_token = jwt.encode({
            'email': user.email,
            'name': user.first_name,
            'sub': user.external_identifier,
        }, self.private_key, self.AUTHORIZATION_ALGO)
        rsa_public_key = rsa.PublicKey.load_pkcs1(self.public_key)
        str_to_be_encrypted = json.dumps({'sub': user.external_identifier})
        enc_message = rsa.encrypt(str_to_be_encrypted.encode(), rsa_public_key)
        enc_string = enc_message.hex()
        refresh_token = jwt.encode({
            'value': enc_string,
        }, self.private_key, self.AUTHORIZATION_ALGO)

        return access_token, refresh_token, id_token
