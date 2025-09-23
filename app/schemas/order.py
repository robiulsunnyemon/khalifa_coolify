from pydantic import BaseModel,ConfigDict
from typing import List, Optional
from datetime import datetime


# ---- OrderItem Schemas ----
class OrderItemBase(BaseModel):
    food_id: int
    user_id: int
    order_id: Optional[int] = None


class Food(BaseModel):
    name: str
    description: Optional[str] = None
    food_image_url: Optional[str] = None
    price: float
    per_person: Optional[int] = None
    category_id: int


class OrderItemCreate(BaseModel):
    food_id: int





class OrderItemResponse(BaseModel):
    id: int
    food: Optional[Food] = None


    model_config = ConfigDict(from_attributes=True)


# ---- Order Schemas ----
class OrderBase(BaseModel):
    total_amount: float
    delivery_address: str
    delivery_full_address: str


class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    order_items: List[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
