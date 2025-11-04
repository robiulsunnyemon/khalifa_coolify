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
def get_payment_by_user_token(
        user: dict = Depends(get_user_info),
        db: Session = Depends(get_db)
):
    try:
        user_id = user["user_id"]
        payments = db.query(PaymentHistoryModel).filter(PaymentHistoryModel.user_id == user_id).all()

        if not payments:
            # Return empty list instead of 404 for no payments found
            return []

        return payments
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving payments: {str(e)}"
        )


# Get Payment by id
@router.get("/{payment_id}", response_model=PaymentResponse, status_code=status.HTTP_200_OK)
def get_payment_by_payment_id(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(PaymentHistoryModel).filter(PaymentHistoryModel.id == payment_id).first()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment with ID {payment_id} not found"
        )

    return payment