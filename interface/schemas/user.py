from uuid import UUID

from pydantic import BaseModel, EmailStr


class CreateClientUserBody(BaseModel):
    client_id: UUID
    temp_password: str


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    phone: str
    password: str


class UserRegisterResponse(BaseModel):
    email: str
    phone: str
    name: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: UUID
    email: str
    phone: str
    name: str
    is_client: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
