
## app.models.food_category.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.db import Base

class FoodCategoryModel(Base):
    __tablename__ = 'food_categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,unique=True, index=True)
    description = Column(String,default="")
    category_image_url = Column(String,default="https://picsum.photos/100/100?random=5")
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), server_onupdate=func.now())


    foods = relationship("FoodModel", back_populates="category", cascade="all, delete-orphan")
