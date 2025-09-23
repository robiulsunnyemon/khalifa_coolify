from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.db import get_db
from app.models.variation_of_food import VariationOfFoodModel
from app.schemas.variation_of_food import VariationOfFoodCreate, VariationOfFoodResponse, VariationOfFoodUpdate

router = APIRouter(
    prefix="/variations",
    tags=["Variations"]
)

# ---------- Create ----------
@router.post("/", response_model=VariationOfFoodResponse)
def create_variation(variation: VariationOfFoodCreate, db: Session = Depends(get_db)):
    db_variation = VariationOfFoodModel(**variation.model_dump())
    db.add(db_variation)
    db.commit()
    db.refresh(db_variation)
    return db_variation

# ---------- Read All ----------
@router.get("/", response_model=List[VariationOfFoodResponse])
def get_variations(db: Session = Depends(get_db)):
    return db.query(VariationOfFoodModel).all()

# ---------- Read One ----------
@router.get("/food_id/{food_id}", response_model=List[VariationOfFoodResponse])
def get_variation(food_id: int, db: Session = Depends(get_db)):
    variation = db.query(VariationOfFoodModel).filter(VariationOfFoodModel.food_id == food_id).all()
    if not variation:
        raise HTTPException(status_code=404, detail="Variation not found")
    return variation





# ---------- Update ----------
@router.put("/{variation_id}", response_model=VariationOfFoodResponse)
def update_variation(variation_id: int, variation_update: VariationOfFoodUpdate, db: Session = Depends(get_db)):
    variation = db.query(VariationOfFoodModel).filter(VariationOfFoodModel.id == variation_id).first()
    if not variation:
        raise HTTPException(status_code=404, detail="Variation not found")
    for key, value in variation_update.model_dump(exclude_unset=True).items():
        setattr(variation, key, value)
    db.commit()
    db.refresh(variation)
    return variation

# ---------- Delete ----------
@router.delete("/{variation_id}")
def delete_variation(variation_id: int, db: Session = Depends(get_db)):
    variation = db.query(VariationOfFoodModel).filter(VariationOfFoodModel.id == variation_id).first()
    if not variation:
        raise HTTPException(status_code=404, detail="Variation not found")
    db.delete(variation)
    db.commit()
    return {"detail": "Variation deleted successfully"}
