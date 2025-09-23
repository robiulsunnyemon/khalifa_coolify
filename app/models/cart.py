from sqlalchemy import Column,Integer,ForeignKey,DateTime
from app.db.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class CartModel(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True,index=True)
    product_id = Column(Integer, ForeignKey("foods.id", ondelete="CASCADE"))
    quantity = Column(Integer,default=1)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(),default=func.now())

    food=relationship("FoodModel", back_populates="cart")