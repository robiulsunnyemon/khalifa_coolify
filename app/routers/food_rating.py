from fastapi import APIRouter, Depends,HTTPException,status
from app.schemas.food_rating import FoodRatingResponse, FoodRatingCreate, FoodRatingResponseForPopularFood
from app.db.db import get_db
from app.models.food_rating import FoodRatingModel
from app.models.food import FoodModel
from typing import List
from sqlalchemy.orm import Session


router = APIRouter(prefix="/food_rating", tags=["Food Rating"])


@router.post("/", response_model=FoodRatingResponse, status_code=status.HTTP_201_CREATED)
async def create_food_rating(food_data: FoodRatingCreate, db: Session = Depends(get_db)):
    db_food = db.query(FoodModel).filter(FoodModel.id == food_data.food_id).first()
    if not db_food:
        raise HTTPException(status_code=404, detail="Food not found")

    food_rating = db.query(FoodRatingModel).filter(FoodRatingModel.food_id == food_data.food_id).first()

    if not food_rating:
        food_rating = FoodRatingModel(
            food_id=food_data.food_id,
            total_ratings=food_data.stars,
            total_rating_users=1,
            average_rating=food_data.stars
        )
        db.add(food_rating)
    else:
        food_rating.total_ratings += food_data.stars
        food_rating.total_rating_users += 1
        food_rating.average_rating = (
            food_rating.total_ratings / food_rating.total_rating_users
        )

    db.commit()
    db.refresh(food_rating)
    return food_rating



@router.get("/{food_id}", response_model=FoodRatingResponse, status_code=status.HTTP_200_OK)
def get_food_rating(food_id: int, db: Session = Depends(get_db)):
    db_food = db.query(FoodRatingModel).filter(FoodRatingModel.food_id == food_id).first()
    if not db_food:
        raise HTTPException(status_code=404, detail="Food not found")
    return db_food


@router.get("/filter/popular", response_model=List[FoodRatingResponseForPopularFood],status_code=status.HTTP_200_OK)
def get_popular_foods(db: Session = Depends(get_db)):
    popular_foods = db.query(FoodRatingModel).filter(FoodRatingModel.food_id > 4).all()
    if not popular_foods:
        raise HTTPException(status_code=404, detail="Food not found")
    return popular_foods