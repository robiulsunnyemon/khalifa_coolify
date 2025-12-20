from pydantic import BaseModel,ConfigDict
from typing import List, Optional
from datetime import datetime


# ---- OrderItem Schemas ----
class OrderItemBase(BaseModel):
    food_id: int
    user_id: int
    order_id: Optional[int] = None


class Food(BaseModel):
    id:int
    name: str
    description: Optional[str] = None
    food_image_url: Optional[str] = None
    price: float
    per_person: Optional[int] = None
    category_id: int


class OrderItemCreate(BaseModel):
    variation_id:int  ##new_add
    food_id: int


##new add
class Variation(BaseModel):
    id:int
    name: Optional[str] =None
    price: Optional[float] =None



class OrderItemResponse(BaseModel):
    id: int
    food: Optional[Food] = None
    variation:Optional[Variation]=None  ##new add


    model_config = ConfigDict(from_attributes=True)


# ---- Order Schemas ----
class OrderBase(BaseModel):
    total_amount: float
    phone_number:str
    delivery_address: str
    delivery_full_address: str


class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]


class User(BaseModel):
    first_name:str
    last_name:str
    email:str



class OrderResponse(OrderBase):
    id: int
    status:str
    created_at: datetime
    updated_at: datetime
    user:Optional[User]=None
    order_items: List[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
