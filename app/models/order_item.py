from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from app.db.db import Base


class OrderItemModel(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    food_id = Column(Integer, ForeignKey("foods.id", ondelete="CASCADE"))

    order = relationship("OrderModel", back_populates="order_items")
    food = relationship("FoodModel", back_populates="order_items")
