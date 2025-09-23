from sqlalchemy import Column, ForeignKey, Integer, String,Float
from sqlalchemy.orm import relationship
from app.db.db import Base


class VariationOfFoodModel(Base):
    __tablename__ = 'variation_of_foods'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,default='For 1 person')
    price = Column(Float,default="0.0")
    food_id = Column(Integer, ForeignKey('foods.id',ondelete='CASCADE'))

    food = relationship("FoodModel",back_populates="variations")