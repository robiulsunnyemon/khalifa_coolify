from pydantic import BaseModel,ConfigDict
from datetime import datetime

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    order_id: int
    total_amount: float
    trx_id: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)