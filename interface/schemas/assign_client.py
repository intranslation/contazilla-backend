from pydantic import BaseModel


class AssignClient(BaseModel):
    client_id: str | None = None
