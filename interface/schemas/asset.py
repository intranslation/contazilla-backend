from pydantic import BaseModel


class AssetCreate(BaseModel):
    filename: str | None = None
    url: str
    client_id: str | None = None


class AssetUpdate(BaseModel):
    filename: str | None = None
    url: str
    client_id: str | None = None


class AssetResponse(BaseModel):
    id: str
    filename: str | None
    url: str
    client_id: str | None
    user_id: str

    class Config:
        from_attributes = True


class AssetUpload(BaseModel):
    client_id: str | None
