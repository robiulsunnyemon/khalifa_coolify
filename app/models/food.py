## app.models.food.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float,DateTime
from sqlalchemy.orm import relationship
from app.db.db import Base
from sqlalchemy.sql import func

class FoodModel(Base):
    __tablename__ = "foods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String,default="")
    food_image_url = Column(String,default="https://picsum.photos/100/100?random=5")
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("food_categories.id", ondelete="CASCADE"))
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    # String notation
    category = relationship("FoodCategoryModel", back_populates="foods")
    cart=relationship("CartModel", back_populates="food",cascade="all, delete-orphan")
    food_ratings = relationship("FoodRatingModel", back_populates="food", uselist=False,cascade="all, delete-orphan")
    order_items=relationship("OrderItemModel", back_populates="food",cascade="all, delete-orphan")
    variations=relationship("VariationOfFoodModel", back_populates="food",cascade="all, delete-orphan")