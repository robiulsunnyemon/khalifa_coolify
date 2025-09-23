from sqlalchemy import Column, ForeignKey, Integer, Float,DateTime,String
from sqlalchemy.orm import relationship
from app.db.db import Base
from sqlalchemy.sql import func


class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    total_amount = Column(Float)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    status = Column(String,default="Pending")
    delivery_address = Column(String)
    delivery_full_address=Column(String)

    order_items = relationship(
        "OrderItemModel", back_populates="order", cascade="all, delete-orphan"
    )


