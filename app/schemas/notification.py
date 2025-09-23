from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime


# Base Schema (common fields)
class NotificationBase(BaseModel):
    title: str
    content: str
    image: Optional[str] = "https://cdn.pixabay.com/photo/2022/02/08/02/56/shipping-7000647_1280.png"


# Create Request Schema
class NotificationCreate(NotificationBase):
    pass


# Update Request Schema
class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    is_read: Optional[bool] = None


# Response Schema
class NotificationResponse(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)