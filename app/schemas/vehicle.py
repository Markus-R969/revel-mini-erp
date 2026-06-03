from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Any
from app.models.vehicle import VehicleStatus

class VehicleBase(BaseModel):
    brand: str = Field(..., min_length=1, max_length=100, examples=["Toyota"])
    model: str = Field(..., min_length=1, max_length=100, examples=["Corolla"])
    year: int = Field(..., ge=1950, le=2030, examples=[2024])
    license_plate: str = Field(..., min_length=5, max_length=20, examples=["1234ABC"])
    monthly_cost_cents: int = Field(..., gt=0, description="Precio mensual en céntimos", examples=[45000])
    status: VehicleStatus = VehicleStatus.AVAILABLE

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: Any
    created_at: datetime
    updated_at: datetime

    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid_to_str(cls, v):
        return str(v) if v else v

    class Config:
        from_attributes = True
