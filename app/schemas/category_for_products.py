from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime
from typing import List


class Rating(BaseModel):
    average_rating: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class VariationOfFoodResponse(BaseModel):
    name: Optional[str]
    price: Optional[float]


class Product(BaseModel):
    name: str
    description: Optional[str] = None
    food_image_url: Optional[str] = None
    price: float
    food_ratings: Optional[Rating] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    variations: List[Optional[VariationOfFoodResponse]] = []

class CategoryResponseWithFood(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category_image_url: Optional[str]
    foods: List[Optional[Product]]=[]
    create_time: datetime
    update_time: datetime