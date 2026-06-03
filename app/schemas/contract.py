from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional, Any
from app.models.contract import ContractStatus

class ContractBase(BaseModel):
    customer_id: Any
    vehicle_id: Any
    start_date: date
    end_date: date
    monthly_fee_cents: int = Field(..., gt=0)

    @field_validator('customer_id', 'vehicle_id', mode='before')
    @classmethod
    def convert_uuid_to_str(cls, v):
        return str(v) if v else v

class ContractCreate(ContractBase):
    pass

class ContractResponse(ContractBase):
    id: Any
    status: ContractStatus
    next_billing_date: date
    created_at: datetime

    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid_to_str_response(cls, v):
        return str(v) if v else v

    class Config:
        from_attributes = True
