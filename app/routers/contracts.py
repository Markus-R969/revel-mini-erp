from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.db import get_db
from app.models.contract import Contract, ContractStatus
from app.models.vehicle import Vehicle, VehicleStatus
from app.models.customer import Customer
from app.models.payment import Payment, PaymentStatus
from app.schemas.contract import ContractCreate, ContractResponse

router = APIRouter(prefix="/contracts", tags=["contracts"])

@router.post("/", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
def create_contract(contract_data: ContractCreate, db: Session = Depends(get_db)):
    # Validaciones de negocio
    if contract_data.end_date <= contract_data.start_date:
        raise HTTPException(status_code=400, detail="La fecha de fin debe ser posterior a la de inicio")
    
    vehicle = db.query(Vehicle).filter(Vehicle.id == contract_data.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    if vehicle.status != VehicleStatus.AVAILABLE:
        raise HTTPException(status_code=400, detail="El vehículo no está disponible")
    
    customer = db.query(Customer).filter(Customer.id == contract_data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Crear contrato + cambiar estado del vehículo + generar primer pago (TRANSACCIÓN)
    try:
        # 1. Crear el contrato
        contract = Contract(
            customer_id=contract_data.customer_id,
            vehicle_id=contract_data.vehicle_id,
            status=ContractStatus.ACTIVE,
            start_date=contract_data.start_date,
            end_date=contract_data.end_date,
            monthly_fee_cents=contract_data.monthly_fee_cents,
            next_billing_date=contract_data.start_date
        )
        db.add(contract)
        db.flush()  # Esto genera el ID del contrato sin hacer commit
        
        # 2. Cambiar el estado del vehículo
        vehicle.status = VehicleStatus.RENTED
        
        # 3. Crear el primer pago con el contract_id correcto
        first_payment = Payment(
            contract_id=contract.id,  # Ahora sí tenemos el ID
            amount_cents=contract_data.monthly_fee_cents,
            due_date=contract_data.start_date,
            status=PaymentStatus.PENDING
        )
        db.add(first_payment)
        
        # 4. Hacer commit de toda la transacción
        db.commit()
        db.refresh(contract)
        return contract
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear contrato: {str(e)}")

@router.get("/", response_model=List[ContractResponse])
def list_contracts(status_filter: ContractStatus = None, db: Session = Depends(get_db)):
    query = db.query(Contract)
    if status_filter:
        query = query.filter(Contract.status == status_filter)
    return query.all()

@router.get("/{contract_id}", response_model=ContractResponse)
def get_contract(contract_id: str, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    return contract
