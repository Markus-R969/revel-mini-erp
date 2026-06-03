from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from typing import Any

class CustomerBase(BaseModel):
    email: EmailStr = Field(..., examples=["cliente@email.com"])
    full_name: str = Field(..., min_length=3, max_length=255, examples=["Juan Pérez"])
    dni: str = Field(..., min_length=8, max_length=20, examples=["12345678A"])
    phone: str = Field(..., min_length=9, max_length=20, examples=["+34600123456"])

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: Any
    created_at: datetime

    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid_to_str(cls, v):
        return str(v) if v else v

    class Config:
        from_attributes = True
