from app.adapters.rest.dtos.client_dto import ClientExtendedDTO, ClientOutDTO, ClientInputDTO
from typing import List
from fastapi import APIRouter, Query
from app.business_logic.client_service import ClientService
from app.config.config import Container

router = APIRouter()
client_service: ClientService = Container.client_service()


@router.get("/clients", response_model=List[ClientOutDTO])
def get_clients(limit: int = Query(default=10, lt=100, gt=0), offset: int = Query(default=0, lt=100, ge=0)):
    clients = client_service.get_clients(limit, offset)
    client_dto_list = []
    for client in clients:
        client_dto_list.append(ClientOutDTO.get_dto(client))
    return client_dto_list


@router.post("/client", response_model=ClientExtendedDTO)
def post_client(client_dto: ClientInputDTO):
    client = client_dto.get_client_model()
    client_service.create_new_client(client)
    return ClientExtendedDTO.get_dto(client)


@router.get("/client/{client_id}", response_model=ClientExtendedDTO)
def get_client(client_id: str):
    client = client_service.find_client(client_id)
    return ClientExtendedDTO.get_dto(client)


@router.delete("/client/{client_id}")
def delete_client(client_id: str):
    client_service.delete_client(client_id)
