from sqlalchemy.orm import Session
from app.models.postgres import Asset
from app.schemas.asset import AssetCreate, AssetUpdate

def get_asset(db: Session, asset_id: int):
    """获取单个资产"""
    return db.query(Asset).filter(Asset.id == asset_id).first()

def get_assets(db: Session, skip: int = 0, limit: int = 20):
    """分页获取资产列表"""
    query = db.query(Asset)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"total": total, "items": items}

def create_asset(db: Session, asset: AssetCreate):
    """创建资产"""
    db_asset = Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def update_asset(db: Session, asset_id: int, asset_update: AssetUpdate):
    """更新资产状态"""
    db_asset = get_asset(db, asset_id)
    if db_asset:
        update_data = asset_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_asset, key, value)
        db.commit()
        db.refresh(db_asset)
    return db_asset