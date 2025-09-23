from sqlalchemy import ForeignKey, Column, Integer, DateTime,Float,String
from sqlalchemy.sql import func
from app.db.db import Base



class PaymentHistoryModel(Base):
    __tablename__ = 'payment_histories'
    id = Column(Integer, primary_key=True,index=True)
    total_amount = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'))
    trx_id=Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
