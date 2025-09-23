from sqlalchemy import Column, Integer, String,DateTime,Float
from sqlalchemy.sql import func
from app.db.db import Base


class MenuModel(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,unique=True,index=True)
    menu_image = Column(String,default='https://picsum.photos/100/100?random=5')
    price = Column(Float)
    menu_item_list = Column(String,default='')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(),onupdate=func.now())