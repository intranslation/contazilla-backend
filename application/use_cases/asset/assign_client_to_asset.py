from uuid import UUID

from application.ports import AssetRepository, ClientRepository
from domain.entities.asset import Asset


class AssignClientToAsset:
    def __init__(self, asset_repo: AssetRepository, client_repo: ClientRepository) -> None:
        self.asset_repo = asset_repo
        self.client_repo = client_repo

    def execute(self, asset_id: UUID, user_id: UUID, client_id: UUID | None) -> Asset:
        existing = self.asset_repo.get_by_id(asset_id, user_id)
        if existing is None:
            raise ValueError("Asset not found")

        if client_id is not None:
            client = self.client_repo.get_by_id(client_id, user_id)
            if client is None:
                raise ValueError("Client not found")

        return self.asset_repo.assign_client(asset_id, user_id, client_id)
