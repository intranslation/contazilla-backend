from pydantic import BaseModel


class AddressCreate(BaseModel):
    street: str | None = None
    zip_code: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    client_id: str | None = None
    company_id: str | None = None


class AddressUpdate(BaseModel):
    street: str | None = None
    zip_code: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    client_id: str | None = None
    company_id: str | None = None


class AddressResponse(BaseModel):
    id: str
    street: str | None
    zip_code: str | None
    city: str | None
    state: str | None
    country: str | None
    client_id: str | None
    company_id: str | None

    class Config:
        from_attributes = True
