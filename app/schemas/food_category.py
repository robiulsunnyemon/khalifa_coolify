from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime


class FoodCategoryCreate(BaseModel):
    name: str
    description: str
    category_image_url: str


class FoodCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_image_url: Optional[str] = None



class FoodCategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category_image_url: Optional[str]
    create_time: datetime
    update_time: datetime

    model_config = ConfigDict(from_attributes=True)
