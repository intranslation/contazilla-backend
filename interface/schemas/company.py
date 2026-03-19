from pydantic import BaseModel

from interface.schemas.address import AddressResponse


class CompanyCreate(BaseModel):
    name: str
    address_id: str | None = None
    cnpj: str
    client_id: str | None = None


class CompanyUpdate(BaseModel):
    name: str
    address_id: str | None = None
    cnpj: str
    client_id: str | None = None


class CompanyResponse(BaseModel):
    id: str
    name: str
    address: AddressResponse | None
    cnpj: str
    client_id: str | None
    user_id: str

    class Config:
        from_attributes = True
