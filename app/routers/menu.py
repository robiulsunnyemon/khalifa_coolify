import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
from app.db.db import get_db
from app.models.menu import MenuModel
from app.schemas.menu import MenuCreate, MenuUpdate, MenuOut

router = APIRouter(
    prefix="/menus",
    tags=["Menu"]
)

# Upload directory for menu images
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads/menu")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------- Create ----------
@router.post("/", response_model=MenuOut, status_code=status.HTTP_201_CREATED)
async def create_menu(
        request: Request,
        name: str = Form(...),
        price: float = Form(...),
        menu_item_list: str = Form(""),
        image: UploadFile = None,
        db: Session = Depends(get_db),
):
    image_url = "https://picsum.photos/100/100?random=5"  # default
    if image and image.filename:
        file_ext = image.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as f:
            f.write(await image.read())

        base_url = str(request.base_url)
        image_url = f"{base_url}uploads/menu/{unique_filename}"

    db_menu = MenuModel(
        name=name,
        price=price,
        menu_item_list=menu_item_list,
        menu_image=image_url
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


# ---------- Bulk Create ----------
@router.post("/bulk", response_model=List[MenuOut], status_code=status.HTTP_201_CREATED)
async def create_menus_bulk(menu_data: List[MenuCreate], db: Session = Depends(get_db)):
    created_menus = []

    for item in menu_data:
        db_menu = MenuModel(
            name=item.name,
            price=item.price,
            menu_item_list=item.menu_item_list,
            menu_image=item.menu_image or "https://picsum.photos/100/100?random=5"
        )
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        created_menus.append(db_menu)

    return created_menus


# ---------- Get all ----------
@router.get("/", response_model=List[MenuOut], status_code=status.HTTP_200_OK)
async def get_all_menus(db: Session = Depends(get_db)):
    menus = db.query(MenuModel).all()
    return menus


# ---------- Get single ----------
@router.get("/{menu_id}", response_model=MenuOut, status_code=status.HTTP_200_OK)
async def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu


# ---------- Update ----------
@router.put("/{menu_id}", response_model=MenuOut, status_code=status.HTTP_200_OK)
async def update_menu(
        menu_id: int,
        data: MenuUpdate,
        db: Session = Depends(get_db)
):
    menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(menu, key, value)

    db.commit()
    db.refresh(menu)
    return menu


# ---------- Delete ----------
@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    db.delete(menu)
    db.commit()
    return {"message": "Menu deleted successfully"}
