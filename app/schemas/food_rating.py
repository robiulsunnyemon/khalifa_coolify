from pydantic import BaseModel,ConfigDict
from typing import Optional,List

from app.schemas.category_for_products import Product


class FoodRatingCreate(BaseModel):
    food_id: int
    stars: int


class FoodRatingResponse(BaseModel):
    food_id: int
    average_rating: float

    model_config = ConfigDict(from_attributes=True)


class FoodBase(BaseModel):
    name: str
    description: Optional[str] = None
    food_image_url: Optional[str] = None
    price: float
    category_id: int

class VariationOfFoodResponse(BaseModel):
    name: Optional[str]
    price: Optional[float]


class FoodRatingResponseForPopularFood(BaseModel):
    food_id: int
    average_rating: float
    ##food: Optional[FoodBase]
    food: List[Optional[Product]]=[]


    model_config = ConfigDict(from_attributes=True)