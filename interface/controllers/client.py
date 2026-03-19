from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.use_cases.client import (CreateClient, DeleteClient,
                                          GetClient, ListClients, UpdateClient)
from domain.entities.user import User
from interface.deps import (create_client_use_case, delete_client_use_case,
                            get_client_use_case, get_current_user_use_case,
                            list_clients_use_case, update_client_use_case)
from interface.schemas import ClientCreate, ClientResponse, ClientUpdate

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: ClientCreate,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[CreateClient, Depends(create_client_use_case)],
):
    try:
        client = use_case.execute(
            name=data.name,
            cpf=data.cpf,
            phone=data.phone,
            email=data.email,
            user_id=current_user.id,
            is_premium=data.is_premium,
        )
        return ClientResponse(
            id=str(client.id),
            name=client.name,
            cpf=client.cpf,
            email=client.email,
            phone=client.phone,
            is_premium=client.is_premium,
            user_id=str(client.user_id),
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.get("/", response_model=list[ClientResponse])
def list_all(
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[ListClients, Depends(list_clients_use_case)],
):
    clients = use_case.execute(user_id=current_user.id)
    return [
        ClientResponse(
            id=str(c.id),
            name=c.name,
            cpf=c.cpf,
            email=c.email,
            phone=c.phone,
            is_premium=c.is_premium,
            user_id=str(c.user_id),
        )
        for c in clients
    ]


@router.get("/{client_id}", response_model=ClientResponse)
def get_by_id(
    client_id: UUID,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[GetClient, Depends(get_client_use_case)],
):
    try:
        client = use_case.execute(client_id=client_id, user_id=current_user.id)
        return ClientResponse(
            id=str(client.id),
            name=client.name,
            cpf=client.cpf,
            email=client.email,
            phone=client.phone,
            is_premium=client.is_premium,
            user_id=str(client.user_id),
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.put("/{client_id}", response_model=ClientResponse)
def update(
    client_id: UUID,
    data: ClientUpdate,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[UpdateClient, Depends(update_client_use_case)],
):
    try:
        client = use_case.execute(
            client_id=client_id,
            user_id=current_user.id,
            name=data.name,
            cpf=data.cpf,
            email=data.email,
            phone=data.phone,
            is_premium=data.is_premium,
        )
        return ClientResponse(
            id=str(client.id),
            name=client.name,
            cpf=client.cpf,
            email=client.email,
            phone=client.phone,
            is_premium=client.is_premium,
            user_id=str(client.user_id),
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    client_id: UUID,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[DeleteClient, Depends(delete_client_use_case)],
):
    try:
        use_case.execute(client_id=client_id, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
