from uuid import UUID

from application.ports import AssetRepository
from domain.entities.asset import Asset


class CreateAsset:
    def __init__(self, asset_repo: AssetRepository) -> None:
        self.asset_repo = asset_repo

    def execute(self, filename: str | None, url: str, client_id: UUID | None, user_id: UUID) -> Asset:
        new_asset = Asset(
            id=None,
            filename=filename,
            url=url,
            client_id=client_id,
            user_id=user_id,
        )
        try:
            return self.asset_repo.create(new_asset)
        except Exception:
            raise ValueError("Error while creating asset")
