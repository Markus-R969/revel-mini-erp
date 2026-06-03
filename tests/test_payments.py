import pytest

def test_payment_idempotency(client):
    """Test: Idempotencia en pagos (crítico para REVEL)"""
    # Crear vehículo, cliente y contrato
    vehicle = client.post("/vehicles/", json={
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2024,
        "license_plate": "PAY001",
        "monthly_cost_cents": 45000
    })
    vehicle_id = vehicle.json()["id"]
    
    customer = client.post("/customers/", json={
        "email": "payment_test@email.com",
        "full_name": "Payment Test",
        "dni": "88888888G",
        "phone": "+34600888888"
    })
    customer_id = customer.json()["id"]
    
    contract = client.post("/contracts/", json={
        "customer_id": customer_id,
        "vehicle_id": vehicle_id,
        "start_date": "2026-06-04",
        "end_date": "2027-06-04",
        "monthly_fee_cents": 45000
    })
    
    # Obtener el pago pendiente
    payments = client.get("/payments/")
    pending_payment = next(p for p in payments.json() if p["status"] == "pending")
    payment_id = pending_payment["id"]
    
    # Marcar como pagado (primera vez)
    response1 = client.post(f"/payments/{payment_id}/mark-paid?stripe_payment_id=pi_test_001")
    assert response1.status_code == 200
    assert response1.json()["status"] == "paid"
    
    # Intentar marcar como pagado otra vez (debe fallar por idempotencia)
    response2 = client.post(f"/payments/{payment_id}/mark-paid?stripe_payment_id=pi_test_001")
    assert response2.status_code == 400
    assert "idempotencia" in response2.json()["detail"]

def test_mark_payment_not_found(client):
    """Test: Intentar marcar un pago que no existe"""
    response = client.post("/payments/00000000-0000-0000-0000-000000000000/mark-paid?stripe_payment_id=pi_test")
    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"]
