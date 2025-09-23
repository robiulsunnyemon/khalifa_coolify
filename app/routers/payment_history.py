from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.db import get_db
from app.models.payment_history import PaymentHistoryModel
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
@router.get("/me",  status_code=status.HTTP_200_OK)
def get_payment_by_user_token(user: dict = Depends(get_user_info), db: Session = Depends(get_db)):
    user_id = user["user_id"]
    payments = db.query(PaymentHistoryModel).filter(PaymentHistoryModel.user_id == user_id).all()
    if not payments:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payments