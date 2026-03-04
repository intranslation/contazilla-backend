from uuid import UUID

from application.ports import AssetRepository
from domain.entities.asset import Asset


class UpdateAsset:
    def __init__(self, asset_repo: AssetRepository) -> None:
        self.asset_repo = asset_repo

    def execute(
        self, asset_id: UUID, user_id: UUID, filename: str | None, url: str, client_id: UUID | None
    ) -> Asset:
        existing = self.asset_repo.get_by_id(asset_id, user_id)
        if existing is None:
            raise ValueError("Asset not found")

        updated_asset = Asset(
            id=asset_id,
            filename=filename,
            url=url,
            client_id=client_id,
            user_id=user_id,
        )
        try:
            return self.asset_repo.update(updated_asset)
        except Exception:
            raise ValueError("Error while updating asset")
