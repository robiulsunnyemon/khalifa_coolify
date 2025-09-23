from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.db import Base


class NotificationModel(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True,default='')
    content = Column(String, nullable=False,default="")
    image = Column(
        String,
        default="https://cdn.pixabay.com/photo/2022/02/08/02/56/shipping-7000647_1280.png",
        nullable=False
    )
    is_read = Column(Boolean, default=False)  

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
