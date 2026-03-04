from uuid import UUID
from sqlalchemy.orm import Session

from domain.entities.asset import Asset
from application.ports import AssetRepository as AssetRepositoryContract
from infrastructure.models.asset import Asset as AssetModel


class AssetRepository(AssetRepositoryContract):
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def create(self, asset: Asset) -> Asset:
        new_asset = AssetModel(
            filename=asset.filename,
            url=asset.url,
            client_id=asset.client_id,
            user_id=asset.user_id,
        )
        self.db.add(new_asset)
        self.db.commit()
        self.db.refresh(new_asset)
        return new_asset.to_domain()

    def get_by_id(self, asset_id: UUID, user_id: UUID) -> Asset | None:
        asset = (
            self.db.query(AssetModel)
            .filter(AssetModel.id == asset_id, AssetModel.user_id == user_id)
            .first()
        )
        if asset is None:
            return None
        return asset.to_domain()

    def list_by_user(self, user_id: UUID) -> list[Asset]:
        assets = (
            self.db.query(AssetModel)
            .filter(AssetModel.user_id == user_id)
            .all()
        )
        return [a.to_domain() for a in assets]

    def update(self, asset: Asset) -> Asset:
        db_asset = (
            self.db.query(AssetModel)
            .filter(AssetModel.id == asset.id, AssetModel.user_id == asset.user_id)
            .first()
        )
        if db_asset is None:
            raise ValueError("Asset not found")

        db_asset.filename = asset.filename
        db_asset.url = asset.url
        db_asset.client_id = asset.client_id
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset.to_domain()

    def delete(self, asset_id: UUID, user_id: UUID) -> None:
        db_asset = (
            self.db.query(AssetModel)
            .filter(AssetModel.id == asset_id, AssetModel.user_id == user_id)
            .first()
        )
        if db_asset is None:
            raise ValueError("Asset not found")
        self.db.delete(db_asset)
        self.db.commit()

    def assign_client(self, asset_id: UUID, user_id: UUID, client_id: UUID | None) -> Asset:
        db_asset = (
            self.db.query(AssetModel)
            .filter(AssetModel.id == asset_id, AssetModel.user_id == user_id)
            .first()
        )
        if db_asset is None:
            raise ValueError("Asset not found")
        db_asset.client_id = client_id
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset.to_domain()
