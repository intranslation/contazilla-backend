from pydantic import BaseModel


class ClientCreate(BaseModel):
    name: str | None = None
    cpf: str
    phone: str | None = None


class ClientUpdate(BaseModel):
    name: str | None = None
    cpf: str
    phone: str | None = None


class ClientResponse(BaseModel):
    id: str
    name: str | None
    cpf: str
    phone: str | None
    user_id: str

    class Config:
        from_attributes = True
