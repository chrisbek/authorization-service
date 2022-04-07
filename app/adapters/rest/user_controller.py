from app.adapters.rest.dtos.user_dto import UserDTO
from typing import List
from fastapi import APIRouter, Query
from app.business_logic.user_service import UserService
from app.config.config import Container

router = APIRouter()
user_service: UserService = Container.user_service()


@router.get("/users", response_model=List[UserDTO])
def get_users(limit: int = Query(default=10, lt=100, gt=0), offset: int = Query(default=0, lt=100, ge=0)):
    users = user_service.get_users(limit, offset)
    user_dto_list = []
    for user in users:
        user_dto_list.append(UserDTO.get_dto(user))
    return user_dto_list


@router.post("/user", response_model=UserDTO)
def post_user(user_dto: UserDTO):
    user = user_dto.get_user_model()
    created_user = user_service.create_new_user(user)
    return UserDTO.get_dto(created_user)


@router.get("/user/{email}", response_model=UserDTO)
def get_user(email: str):
    user = user_service.find_user(email)
    return UserDTO.get_dto(user)


@router.delete("/user/{email}")
def delete_user(email: str):
    user_service.delete_user(email)
