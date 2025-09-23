from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.db import get_db
from app.models.order import OrderModel
from app.models.order_item import OrderItemModel
from app.schemas.order import OrderCreate, OrderResponse
from app.utils.user_info import get_user_info

router = APIRouter(prefix="/orders", tags=["Orders"])


# Create Order
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db),user: dict = Depends(get_user_info)):
    user_id = user["user_id"]
    new_order = OrderModel(
        user_id=user_id,
        total_amount=order_data.total_amount,
        delivery_address=order_data.delivery_address,
        delivery_full_address=order_data.delivery_full_address,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)


    for item in order_data.order_items:
        order_item = OrderItemModel(
            user_id=order_data.user_id,
            order_id=new_order.id,
            food_id=item.food_id,
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)

    return new_order


# Get all orders
@router.get("/", response_model=List[OrderResponse],status_code=status.HTTP_200_OK)
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(OrderModel).all()


# Get order by ID
@router.get("/{order_id}", response_model=OrderResponse,status_code=status.HTTP_200_OK)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# Get order by ID
@router.get("/user/me", response_model=List[OrderResponse],status_code=status.HTTP_200_OK)
def get_order( user: dict = Depends(get_user_info), db: Session = Depends(get_db)):
    user_id = user["user_id"]
    orders = db.query(OrderModel).filter(OrderModel.user_id == user_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders




# Get order by user_id
@router.get("/user/{user_id}",response_model=List[OrderResponse],status_code=status.HTTP_200_OK)
def get_order(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(OrderModel).filter(OrderModel.user_id == user_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders





# Delete order
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
