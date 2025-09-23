from pydantic import BaseModel,ConfigDict
from typing import Optional,List


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


class FoodRatingResponseForPopularFood(BaseModel):
    food_id: int
    average_rating: float
    food: Optional[FoodBase]


    model_config = ConfigDict(from_attributes=True)