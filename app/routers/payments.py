from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db import get_db
from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentResponse

router = APIRouter(prefix="/payments", tags=["payments"])

@router.get("/", response_model=List[PaymentResponse])
def list_payments(status_filter: PaymentStatus = None, db: Session = Depends(get_db)):
    query = db.query(Payment)
    if status_filter:
        query = query.filter(Payment.status == status_filter)
    return query.all()

@router.post("/{payment_id}/mark-paid", response_model=PaymentResponse)
def mark_payment_paid(payment_id: str, stripe_payment_id: str = None, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    if payment.status == PaymentStatus.PAID:
        raise HTTPException(status_code=400, detail="El pago ya está marcado como pagado (idempotencia)")
    
    payment.status = PaymentStatus.PAID
    payment.paid_at = datetime.utcnow()
    if stripe_payment_id:
        payment.stripe_payment_id = stripe_payment_id
    
    db.commit()
    db.refresh(payment)
    return payment
