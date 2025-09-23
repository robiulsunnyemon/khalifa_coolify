from sqlalchemy import Column,Integer, ForeignKey,Float
from app.db.db import Base
from sqlalchemy.orm import relationship



class FoodRatingModel(Base):
    __tablename__ = "food_ratings"
    id = Column(Integer, primary_key=True,index=True)
    total_ratings = Column(Integer,default=5)
    total_rating_users=Column(Integer,default=1)
    average_rating = Column(Float,default=5.0)
    food_id = Column(Integer, ForeignKey("foods.id", ondelete="CASCADE"))


    food = relationship("FoodModel", back_populates="food_ratings")