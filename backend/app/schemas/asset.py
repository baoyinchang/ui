from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class AssetBase(BaseModel):
    name: str = Field(..., max_length=100)
    ip: str = Field(..., max_length=45)
    type: Optional[str] = Field(None, max_length=50)
    os: Optional[str] = Field(None, max_length=100)

class AssetCreate(AssetBase):
    pass  # 创建时无需ID和时间

class AssetUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(online|offline)$")
    last_checkin: Optional[datetime] = None

class AssetInDB(AssetBase):
    id: int
    status: str = "online"
    last_checkin: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True  # 适配SQLAlchemy模型

class AssetListResponse(BaseModel):
    total: int
    items: List[AssetInDB]