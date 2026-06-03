import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db import Base

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    OVERDUE = "overdue"

class Payment(Base):
    __tablename__ = "payments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=False)
    amount_cents = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    paid_at = Column(DateTime, nullable=True)
    status = Column(SAEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    stripe_payment_id = Column(String(255), unique=True, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    contract = relationship("Contract", back_populates="payments")
