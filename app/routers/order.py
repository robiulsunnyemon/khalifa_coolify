from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.db import get_db
from app.models.order import OrderModel
from app.models.order_item import OrderItemModel
from app.models.payment_history import PaymentHistoryModel
from app.schemas.order import OrderCreate, OrderResponse
from app.utils.user_info import get_user_info
from app.models.cart import CartModel
from sqlalchemy import and_

router = APIRouter(prefix="/orders", tags=["Orders"])



@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db), user: dict = Depends(get_user_info)):
    user_id = user["user_id"]

    db_order = db.query(OrderModel).filter(
        OrderModel.user_id == user_id,
        OrderModel.status == "Pending"
    ).first()
    if db_order:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Order already exists")

    new_order = OrderModel(
        user_id=user_id,
        total_amount=order_data.total_amount,
        delivery_address=order_data.delivery_address,
        delivery_full_address=order_data.delivery_full_address,
        phone_number=order_data.phone_number,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order_data.order_items:
        order_item = OrderItemModel(
            user_id=user_id,  # fixed
            order_id=new_order.id,
            food_id=item.food_id,
            variation_id=item.variation_id  ##new_add
        )
        db.add(order_item)

        cart_item = db.query(CartModel).filter(
            and_(CartModel.product_id == item.food_id, CartModel.user_id == user_id)
        ).first()
        if cart_item:
            db.delete(cart_item)

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
##, response_model=List[OrderResponse]  new add
@router.get("/user/me",response_model=List[OrderResponse],status_code=status.HTTP_200_OK)
def get_order( user: dict = Depends(get_user_info), db: Session = Depends(get_db)):
    user_id = user["user_id"]
    orders = db.query(OrderModel).filter(OrderModel.user_id == user_id).all()
    return orders


@router.get("/user/me/latest", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def get_latest_order(user: dict = Depends(get_user_info), db: Session = Depends(get_db)):
    user_id = user["user_id"]
    latest_order = (
        db.query(OrderModel)
        .filter(OrderModel.user_id == user_id)
        .order_by(OrderModel.created_at.desc())  # অথবা .order_by(OrderModel.id.desc())
        .first()
    )

    if not latest_order:
        raise HTTPException(status_code=404, detail="No orders found for this user")

    return latest_order


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


@router.put("/complete/{order_id}", status_code=status.HTTP_200_OK)
def update_order_status_active(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = "Complete"
    payment_history = PaymentHistoryModel(
        order_id=order_id,
        total_amount=order.total_amount,
        user_id=order.user_id,
        trx_id="cash_on_delivery",
    )
    db.add(payment_history)
    db.commit()
    db.refresh(order)
    return {"message": "Order status updated to Complete"}


# Delete all orders
@router.delete("/all/delete", status_code=status.HTTP_200_OK)
def delete_all_orders(db: Session = Depends(get_db)):
    try:
        # প্রথমে OrderItemModel থেকে সব ডাটা ডিলিট করতে হবে কারণ এটি Foreign Key দিয়ে যুক্ত
        db.query(OrderItemModel).delete()

        # এরপর OrderModel ডিলিট করুন
        num_deleted = db.query(OrderModel).delete()

        db.commit()
        return {"message": f"Successfully deleted {num_deleted} orders and their items."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )