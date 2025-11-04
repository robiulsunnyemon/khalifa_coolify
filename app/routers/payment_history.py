from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.db import get_db
from app.models.order import OrderModel
from app.models.payment_history import PaymentHistoryModel
from app.schemas.order import OrderResponse
from app.schemas.payment_history import PaymentResponse
from app.utils.user_info import get_user_info

router = APIRouter(
    prefix="/payment_history",
    tags=["Payments_Histroy"]
)


# Get All Payments
@router.get("/", response_model=List[PaymentResponse], status_code=status.HTTP_200_OK)
def get_payments(db: Session = Depends(get_db)):
    payments = db.query(PaymentHistoryModel).all()
    return payments

# Get Payment by user_id
@router.get("/{user_id}", response_model=List[PaymentResponse], status_code=status.HTTP_200_OK)
def get_payment_by_user_id(user_id: int, db: Session = Depends(get_db)):
    payments = db.query(PaymentHistoryModel).filter(PaymentHistoryModel.user_id == user_id).all()
    if not payments:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payments


# Get Payment by  me
@router.get("/me", response_model=List[PaymentResponse], status_code=status.HTTP_200_OK)
def get_payment_by_user_token(user: dict = Depends(get_user_info), db: Session = Depends(get_db)):
    user_id = 2
    payments = db.query(PaymentHistoryModel).filter(PaymentHistoryModel.user_id == user_id).all()
    if not payments:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payments



# Get Payment by id
@router.get("/{payment_id}",response_model=OrderResponse, status_code=status.HTTP_200_OK)
def get_payment_by_payment_id(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(PaymentHistoryModel).filter(PaymentHistoryModel.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    order = db.query(OrderModel).filter(OrderModel.id ==payment.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
