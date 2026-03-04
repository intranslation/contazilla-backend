from uuid import UUID

from application.ports import AssetRepository


class DeleteAsset:
    def __init__(self, asset_repo: AssetRepository) -> None:
        self.asset_repo = asset_repo

    def execute(self, asset_id: UUID, user_id: UUID) -> None:
        existing = self.asset_repo.get_by_id(asset_id, user_id)
        if existing is None:
            raise ValueError("Asset not found")
        self.asset_repo.delete(asset_id, user_id)
