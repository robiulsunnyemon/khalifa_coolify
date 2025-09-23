from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime

class MenuBase(BaseModel):
    name: str
    price: float
    menu_image: Optional[str] = "https://picsum.photos/100/100?random=5"
    menu_item_list: Optional[str] = ""

class MenuCreate(MenuBase):
    pass

class MenuUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    menu_image: Optional[str] = None
    menu_item_list: Optional[str] = None

class MenuOut(MenuBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
