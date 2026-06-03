import pytest

def test_create_contract_success(client):
    """Test: Crear un contrato correctamente (transacción atómica)"""
    # Crear vehículo
    vehicle_response = client.post("/vehicles/", json={
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2024,
        "license_plate": "CONT001",
        "monthly_cost_cents": 45000
    })
    vehicle_id = vehicle_response.json()["id"]
    
    # Crear cliente
    customer_response = client.post("/customers/", json={
        "email": "test_contract@email.com",
        "full_name": "Test Customer",
        "dni": "12345678A",
        "phone": "+34600123456"
    })
    customer_id = customer_response.json()["id"]
    
    # Crear contrato
    response = client.post("/contracts/", json={
        "customer_id": customer_id,
        "vehicle_id": vehicle_id,
        "start_date": "2026-06-04",
        "end_date": "2027-06-04",
        "monthly_fee_cents": 45000
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "active"
    assert data["customer_id"] == customer_id
    assert data["vehicle_id"] == vehicle_id
    
    # Verificar que el vehículo ahora está RENTED
    vehicle_check = client.get(f"/vehicles/{vehicle_id}")
    assert vehicle_check.json()["status"] == "rented"
    
    # Verificar que se creó un pago pendiente
    payments = client.get("/payments/")
    assert payments.status_code == 200
    payments_data = payments.json()
    assert len(payments_data) > 0
    assert any(p["status"] == "pending" for p in payments_data)

def test_create_contract_vehicle_not_available(client):
    """Test: No se puede crear contrato con vehículo no disponible"""
    # Crear vehículo
    vehicle_response = client.post("/vehicles/", json={
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2024,
        "license_plate": "NAVAIL01",
        "monthly_cost_cents": 45000
    })
    vehicle_id = vehicle_response.json()["id"]
    
    # Crear dos clientes
    customer1 = client.post("/customers/", json={
        "email": "customer1@email.com",
        "full_name": "Customer 1",
        "dni": "11111111A",
        "phone": "+34600111111"
    })
    customer1_id = customer1.json()["id"]
    
    customer2 = client.post("/customers/", json={
        "email": "customer2@email.com",
        "full_name": "Customer 2",
        "dni": "22222222B",
        "phone": "+34600222222"
    })
    customer2_id = customer2.json()["id"]
    
    # Crear primer contrato (éxito)
    client.post("/contracts/", json={
        "customer_id": customer1_id,
        "vehicle_id": vehicle_id,
        "start_date": "2026-06-04",
        "end_date": "2027-06-04",
        "monthly_fee_cents": 45000
    })
    
    # Intentar crear segundo contrato con el mismo vehículo (debe fallar)
    response = client.post("/contracts/", json={
        "customer_id": customer2_id,
        "vehicle_id": vehicle_id,
        "start_date": "2026-06-04",
        "end_date": "2027-06-04",
        "monthly_fee_cents": 45000
    })
    
    assert response.status_code == 400
    assert "no está disponible" in response.json()["detail"]

def test_create_contract_invalid_dates(client):
    """Test: No se puede crear contrato con end_date < start_date"""
    # Crear vehículo
    vehicle_response = client.post("/vehicles/", json={
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2024,
        "license_plate": "DATE001",
        "monthly_cost_cents": 45000
    })
    vehicle_id = vehicle_response.json()["id"]
    
    # Crear cliente
    customer_response = client.post("/customers/", json={
        "email": "date_test@email.com",
        "full_name": "Date Test",
        "dni": "99999999Z",
        "phone": "+34600999999"
    })
    customer_id = customer_response.json()["id"]
    
    # Intentar crear contrato con fechas inválidas
    response = client.post("/contracts/", json={
        "customer_id": customer_id,
        "vehicle_id": vehicle_id,
        "start_date": "2027-06-04",
        "end_date": "2026-06-04",  # Fecha de fin antes de inicio
        "monthly_fee_cents": 45000
    })
    
    assert response.status_code == 400
    assert "fecha de fin debe ser posterior" in response.json()["detail"]
