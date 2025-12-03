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

        base_url = str(request.base_url).replace("http://", "https://")
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
    db_menu.menu_item_list = db_menu.menu_item_list.replace("\\n", "\n")
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

    # Convert \\n to \n for each menu item
    for menu in menus:
        if menu.menu_item_list:
            menu.menu_item_list = menu.menu_item_list.replace("\\n", "\n")

    return menus


# ---------- Get single ----------
@router.get("/{menu_id}", response_model=MenuOut, status_code=status.HTTP_200_OK)
async def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()

    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    # Convert escaped newline \\n to real newline \n
    if menu.menu_item_list:
        menu.menu_item_list = menu.menu_item_list.replace("\\n", "\n")

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


# ---------- Update Menu ----------
@router.patch("/{menu_id}", response_model=MenuOut)
async def update_menu(
        menu_id: int,
        request: Request,
        name: str = Form(None),
        price: float = Form(None),
        menu_item_list: str = Form(None),
        image: UploadFile = None,
        db: Session = Depends(get_db),
):
    # Check if menu exists
    db_menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")

    # Update basic fields if provided
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if price is not None:
        update_data["price"] = price
    if menu_item_list is not None:
        update_data["menu_item_list"] = menu_item_list

    # Handle image update
    if image:
        if image.filename:  # New image provided
            # Delete old image if exists and not default
            if db_menu.menu_image and "picsum.photos" not in db_menu.menu_image:
                # Extract filename from URL if it's our uploaded image
                try:
                    old_filename = db_menu.menu_image.split("/")[-1]
                    old_file_path = os.path.join(UPLOAD_DIR, old_filename)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                except:
                    pass  # If URL parsing fails, ignore

            # Save new image
            file_ext = image.filename.split(".")[-1]
            unique_filename = f"{uuid.uuid4()}.{file_ext}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)

            with open(file_path, "wb") as f:
                f.write(await image.read())

            base_url = str(request.base_url).replace("http://", "https://")
            update_data["menu_image"] = f"{base_url}uploads/menu/{unique_filename}"
        else:
            # If image is sent but empty, set to default
            update_data["menu_image"] = "https://picsum.photos/100/100?random=5"

    # Update the menu record
    if update_data:
        for key, value in update_data.items():
            setattr(db_menu, key, value)

        db.commit()
        db.refresh(db_menu)

    return db_menu