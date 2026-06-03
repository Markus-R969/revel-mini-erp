from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional, Any
from app.models.payment import PaymentStatus

class PaymentBase(BaseModel):
    contract_id: Any
    amount_cents: int = Field(..., gt=0)
    due_date: date

    @field_validator('contract_id', mode='before')
    @classmethod
    def convert_uuid_to_str(cls, v):
        return str(v) if v else v

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: Any
    status: PaymentStatus
    paid_at: Optional[datetime] = None
    stripe_payment_id: Optional[str] = None
    created_at: datetime

    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid_to_str_response(cls, v):
        return str(v) if v else v

    class Config:
        from_attributes = True
