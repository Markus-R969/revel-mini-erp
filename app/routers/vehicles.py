from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db import get_db
from app.models.vehicle import Vehicle, VehicleStatus
from app.schemas.vehicle import VehicleCreate, VehicleResponse

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle_data: VehicleCreate, db: Session = Depends(get_db)):
    # Verificar que la matrícula no exista
    existing = db.query(Vehicle).filter(Vehicle.license_plate == vehicle_data.license_plate).first()
    if existing:
        raise HTTPException(status_code=400, detail="La matrícula ya existe")
    
    vehicle = Vehicle(**vehicle_data.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle

@router.get("/", response_model=List[VehicleResponse])
def list_vehicles(status_filter: VehicleStatus = None, db: Session = Depends(get_db)):
    query = db.query(Vehicle)
    if status_filter:
        query = query.filter(Vehicle.status == status_filter)
    return query.all()

@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: str, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehicle
