
## schemas/cart.py  code

from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime
from typing import List


class CartBase(BaseModel):
    product_id: int
    quantity: int
    user_id: int


class CartCreate(BaseModel):
    product_id: int
    variation_id: int
    quantity: Optional[int] = 1



class CartUpdate(BaseModel):
    quantity: Optional[int] = None


class VariationOfFoodResponse(BaseModel):
    id: int
    name: Optional[str]
    price: Optional[float]

class Food(BaseModel):
    id: int
    name: str
    price: float
    description: str
    food_image_url: Optional[str] = None

class CartResponse(CartBase):
    id: int
    food: Optional[Food] = None
    variation: Optional[VariationOfFoodResponse] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)