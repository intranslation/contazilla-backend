from pydantic import BaseModel


class ClientCreate(BaseModel):
    name: str
    cpf: str | None = None
    phone: str | None = None
    email: str | None = None
    is_premium: bool = False


class ClientUpdate(BaseModel):
    name: str | None = None
    cpf: str | None = None
    phone: str | None = None
    email: str | None = None
    is_premium: bool | None = None


class ClientResponse(BaseModel):
    id: str
    name: str
    cpf: str | None
    email: str | None
    phone: str | None
    is_premium: bool
    user_id: str

    class Config:
        from_attributes = True
