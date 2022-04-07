from uuid import uuid4
from pydantic import BaseModel
from sqlalchemy import UniqueConstraint, Column, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
import string
import random


class ClientRedirectUriLink(SQLModel, table=True):
    __table_args__ = (
        PrimaryKeyConstraint('client_id', 'redirect_uri_id', name='primary_key_constraint'),
    )
    client_id: str = Field(
        default=None, foreign_key="client.client_id", nullable=False
    )
    redirect_uri_id: str = Field(
        default=None, foreign_key="redirect_uris.redirect_uri", nullable=False
    )


class RedirectUri(SQLModel, table=True):
    __tablename__ = "redirect_uris"
    redirect_uri: str = Field(..., primary_key=True, nullable=False)
    client_id: Optional['Client'] = Relationship(back_populates="redirect_urls", link_model=ClientRedirectUriLink)


class Client(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("client_name"),)

    client_name: str
    redirect_urls: List[RedirectUri] = Relationship(
        back_populates="client_id", link_model=ClientRedirectUriLink, sa_relationship_kwargs={'lazy': 'subquery'})
    client_id: str = Field(
        default_factory=lambda: ''.join(random.choices(string.ascii_uppercase + string.digits, k=24)),
        primary_key=True, nullable=False)
    client_secret: str = Field(
        default_factory=lambda: ''.join(random.choices(string.ascii_uppercase + string.digits, k=48)))


class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("email"), UniqueConstraint("external_identifier"),)

    uid: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    first_name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    external_identifier: str = Field(default_factory=lambda: str(uuid4()))


class AuthorizationData(SQLModel, table=True):
    code: str = Field(..., primary_key=True, nullable=False)
    access_token: str = Field(..., sa_column=Column(LONGTEXT))
    refresh_token: str = Field(..., sa_column=Column(LONGTEXT))
    id_token: str = Field(..., sa_column=Column(LONGTEXT))


class WellKnownData(BaseModel):
    public_key: str
    token_endpoint: str
