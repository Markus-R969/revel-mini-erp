import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db import Base

class ContractStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Contract(Base):
    __tablename__ = "contracts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    status = Column(SAEnum(ContractStatus), default=ContractStatus.ACTIVE, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    monthly_fee_cents = Column(Integer, nullable=False)
    next_billing_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    customer = relationship("Customer", back_populates="contracts")
    vehicle = relationship("Vehicle", back_populates="contracts")
    payments = relationship("Payment", back_populates="contract")
