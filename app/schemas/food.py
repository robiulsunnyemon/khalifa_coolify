# app/schemas/food.py
from datetime import datetime
from pydantic import BaseModel,ConfigDict
from typing import Optional, List

class FoodBase(BaseModel):
    name: str
    description: Optional[str] = None
    food_image_url: Optional[str] = None
    price: float
    category_id: int

class FoodCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    food_image_url: Optional[str] = "https://cdn.pixabay.com/photo/2022/02/08/02/56/shipping-7000647_1280.png"

class FoodUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    food_image_url: Optional[str] = None
    category_id: Optional[int] = None

class Category(BaseModel):
    name: str

class Rating(BaseModel):
    average_rating: float = 0.0   # default value set করলাম

    model_config = ConfigDict(from_attributes=True)



class VariationOfFoodResponse(BaseModel):
    name: Optional[str]
    price: Optional[float]

class FoodResponse(FoodBase):
    id: int
    category: Optional[Category]
    food_ratings: Optional[Rating] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    variations: List[Optional[VariationOfFoodResponse]] = []

    model_config = ConfigDict(from_attributes=True)
