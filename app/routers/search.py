from fastapi import APIRouter, Depends, Query,status
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.food import FoodModel
from app.schemas.food import FoodResponse
from typing import List

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/", response_model=List[FoodResponse],status_code=status.HTTP_200_OK)
def search_foods(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    results = db.query(FoodModel).filter(
        (FoodModel.name.ilike(f"%{q}%")) | (FoodModel.description.ilike(f"%{q}%"))
    ).all()
    return results
