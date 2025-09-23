from fastapi import APIRouter, Depends, HTTPException
from app.payment.bkash.payment_create import create_payment
from app.payment.bkash.payment_execute import execute_payment
from app.payment.bkash.bkash_payment_token_generation import get_bkash_token
from app.models.order import OrderModel
from app.db.db import get_db
from sqlalchemy.orm import Session
from app.schemas.payment import PaymentCreate
from app.models.payment_history import PaymentHistoryModel

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/pay-bkash/")
def pay_bkash(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    # 1. Order validate
    db_order = db.query(OrderModel).filter(OrderModel.order_id == payment_data.order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 2. Token fetch
    token_response = get_bkash_token()
    token = token_response.get("id_token")
    if not token:
        raise HTTPException(status_code=500, detail="Failed to get bKash token")

    # 3. Payment create (only with user-given amount)

    payment_response = create_payment(token, payment_data.total_amount)
    payment_id = payment_response.get("paymentID")
    if not payment_id:
        raise HTTPException(status_code=500, detail="Failed to create payment")

    # 4. Payment execute
    execute_response = execute_payment(token, payment_id)

    # 5. If success → update order + save history
    if execute_response.get("transactionStatus") == "Completed":
        db_order.status = "Payment Completed"

        payment_history = PaymentHistoryModel(
            order_id=payment_data.order_id,
            total_amount=execute_response.get("amount"),  # use actual paid amount
            user_id=db_order.user_id,
            trx_id=execute_response.get("trxID"),         # চাইলে transaction ID ও লগ করতে পারো
        )

        db.add(payment_history)
        db.commit()

    return execute_response
