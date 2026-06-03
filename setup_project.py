import os

# Contenido de cada archivo
files = {
    "app/__init__.py": "",
    
    "app/config.py": """from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://revel_user:revel_password@localhost:5432/revel_erp"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
""",
    
    "app/db.py": """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""",
    
    "app/models/__init__.py": """from app.models.vehicle import Vehicle, VehicleStatus
from app.models.customer import Customer
from app.models.contract import Contract, ContractStatus
from app.models.payment import Payment, PaymentStatus

__all__ = [
    "Vehicle",
    "VehicleStatus",
    "Customer",
    "Contract",
    "ContractStatus",
    "Payment",
    "PaymentStatus",
]
""",
    
    "app/models/vehicle.py": """import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db import Base


class VehicleStatus(str, enum.Enum):
    AVAILABLE = "available"
    RENTED = "rented"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"


class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    license_plate = Column(String(20), unique=True, nullable=False, index=True)
    status = Column(SAEnum(VehicleStatus), default=VehicleStatus.AVAILABLE, nullable=False)
    monthly_cost_cents = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    contracts = relationship("Contract", back_populates="vehicle")
    
    def __repr__(self):
        return f"<Vehicle {self.brand} {self.model} ({self.license_plate})>"
""",
    
    "app/models/customer.py": """import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime