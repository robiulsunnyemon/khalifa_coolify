
import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, Form, Request, HTTPException,status
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.food_category import FoodCategoryModel
from app.schemas.category_for_products import CategoryResponseWithFood
from app.models.food import FoodModel
from app.models.food_rating import FoodRatingModel
from app.schemas.food_category import FoodCategoryCreate, FoodCategoryUpdate, FoodCategoryResponse
from typing import List

from app.schemas.food_rating import FoodRatingResponseForPopularFood

router = APIRouter(
    prefix="/food-categories",
    tags=["Food Categories"]
)


UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                          "uploads/category")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------- Create ----------
@router.post("/", response_model=FoodCategoryResponse,status_code=status.HTTP_201_CREATED)
async def create_food_category(
        request: Request,
        name: str = Form(...),
        description: str = Form(None),
        image: UploadFile = None,
        db: Session = Depends(get_db)
):
    image_url = None
    if image and image.filename:

        file_ext = image.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as f:
            f.write(await image.read())


        base_url = str(request.base_url)
        image_url = f"{base_url}uploads/category/{unique_filename}"

    db_category = FoodCategoryModel(
        name=name,
        description=description,
        category_image_url=image_url
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category



# ---------- bulk create food categories ----------
@router.post("/bulk", response_model=List[FoodCategoryResponse],status_code=status.HTTP_201_CREATED)
async def create_food_category_bulk(category_data: List[FoodCategoryCreate], db: Session = Depends(get_db)):

    created_categories = []

    for item in category_data:
        db_category = FoodCategoryModel(
            name=item.name,
            description=item.description,
            category_image_url=item.category_image_url
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        created_categories.append(db_category)

    return created_categories



# ---------- Get all ----------
@router.get("/", response_model=list[FoodCategoryResponse],status_code=status.HTTP_200_OK)
async def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(FoodCategoryModel).all()
    return categories


# ---------- Get single ----------
@router.get("/{category_id}", response_model=FoodCategoryResponse,status_code=status.HTTP_200_OK)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(FoodCategoryModel).filter(FoodCategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category



# ---------- Get Product by name ----------
@router.get("/name/{category_name}",response_model=CategoryResponseWithFood, status_code=status.HTTP_200_OK)
async def get_category_name(category_name: str, db: Session = Depends(get_db)):

    category = db.query(FoodCategoryModel).filter(FoodCategoryModel.name.ilike(category_name)).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# ---------- Update ----------
@router.put("/{category_id}", response_model=FoodCategoryResponse, status_code=status.HTTP_201_CREATED)
async def update_category(category_id: int, data: FoodCategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(FoodCategoryModel).filter(FoodCategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


# ---------- Delete ----------
@router.delete("/{category_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(FoodCategoryModel).filter(FoodCategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}