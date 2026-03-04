from uuid import UUID

from application.ports import AssetRepository
from domain.entities.asset import Asset


class ListAssets:
    def __init__(self, asset_repo: AssetRepository) -> None:
        self.asset_repo = asset_repo

    def execute(self, user_id: UUID) -> list[Asset]:
        return self.asset_repo.list_by_user(user_id)
