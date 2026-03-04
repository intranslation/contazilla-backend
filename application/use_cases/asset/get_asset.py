from uuid import UUID

from application.ports import AssetRepository
from domain.entities.asset import Asset


class GetAsset:
    def __init__(self, asset_repo: AssetRepository) -> None:
        self.asset_repo = asset_repo

    def execute(self, asset_id: UUID, user_id: UUID) -> Asset:
        asset = self.asset_repo.get_by_id(asset_id, user_id)
        if asset is None:
            raise ValueError("Asset not found")
        return asset
