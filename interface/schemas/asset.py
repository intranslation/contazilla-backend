from datetime import datetime

from pydantic import BaseModel


class AssetCreate(BaseModel):
    filename: str | None = None
    client_id: str | None = None
    size: float | None = None


class AssetUpdate(BaseModel):
    filename: str | None = None
    client_id: str | None = None
    was_viewed: bool | None = None
    was_downloaded: bool | None = None


class AssetResponse(BaseModel):
    id: str
    filename: str | None
    client_id: str | None
    user_id: str
    size: float | None
    was_viewed: bool
    was_downloaded: bool
    created_at: None | datetime
    updated_at: None | datetime

    class Config:
        from_attributes = True


class AssetUpload(BaseModel):
    client_id: str | None
