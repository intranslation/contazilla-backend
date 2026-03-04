from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    address: str
    cnpj: str
    client_id: str | None = None


class CompanyUpdate(BaseModel):
    name: str
    address: str
    cnpj: str
    client_id: str | None = None


class CompanyResponse(BaseModel):
    id: str
    name: str
    address: str
    cnpj: str
    client_id: str | None
    user_id: str

    class Config:
        from_attributes = True
