from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.db import get_db
from app.models.cart import CartModel
from app.schemas.cart import CartCreate, CartResponse
from app.utils.user_info import get_user_info

router = APIRouter(
    prefix="/carts",
    tags=["Carts"]
)

# ---------- Add or Update Cart Item ----------
@router.post("/", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def add_or_update_cart(
    cart_product: CartCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_user_info)
):
    user_id = user["user_id"]
    cart_item = db.query(CartModel).filter(
        (CartModel.product_id == cart_product.product_id) &
        (CartModel.user_id == user_id)
    ).first()

    if cart_item:
        cart_item.quantity += cart_product.quantity
    else:
        cart_item = CartModel(
            product_id=cart_product.product_id,
            quantity=cart_product.quantity,
            user_id=user_id
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item


# ---------- Decrease Cart Item ----------
@router.post("/{cart_id}/decrease", response_model=CartResponse,status_code=status.HTTP_201_CREATED)
async def decrease_cart_item(
    cart_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_user_info)
):
    user_id = user["user_id"]
    cart_item = db.query(CartModel).filter(
        (CartModel.id == cart_id) & (CartModel.user_id == user_id)
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        db.commit()
        db.refresh(cart_item)
        return cart_item
    else:

        db.delete(cart_item)
        db.commit()
        return {"message": "Cart item removed from cart"}


# ---------- Get all cart items for current user ----------
@router.get("/me", response_model=List[CartResponse],status_code=status.HTTP_200_OK)
async def get_cart_for_current_user(
    db: Session = Depends(get_db),
    user: dict = Depends(get_user_info)
):
    user_id = user["user_id"]
    cart_items = db.query(CartModel).filter(CartModel.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")
    return cart_items


# ---------- Delete Cart Item ----------
@router.delete("/{cart_id}", status_code=status.HTTP_200_OK)
async def delete_cart_item(
    cart_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_user_info)
):
    user_id = user["user_id"]
    cart_item = db.query(CartModel).filter(
        (CartModel.id == cart_id) & (CartModel.user_id == user_id)
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"message": "Cart item deleted successfully"}
