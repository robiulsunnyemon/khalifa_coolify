from pydantic import BaseModel,ConfigDict
from typing import Optional

class VariationOfFoodBase(BaseModel):
    name: Optional[str] = "For 1 person"
    price: Optional[float] = 0.0
    food_id: int

class VariationOfFoodCreate(VariationOfFoodBase):
    pass

class VariationOfFoodUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]

class VariationOfFoodResponse(VariationOfFoodBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
