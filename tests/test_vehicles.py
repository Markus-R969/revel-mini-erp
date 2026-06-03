import pytest

def test_create_vehicle(client):
    """Test: Crear un vehículo correctamente"""
    response = client.post("/vehicles/", json={
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2024,
        "license_plate": "TEST001",
        "monthly_cost_cents": 45000
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["brand"] == "Toyota"
    assert data["model"] == "Corolla"
    assert data["license_plate"] == "TEST001"
    assert data["status"] == "available"
    assert "id" in data

def test_create_vehicle_duplicate_plate(client):
    """Test: No se puede crear dos vehículos con la misma matrícula"""
    # Crear primer vehículo
    client.post("/vehicles/", json={
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2024,
        "license_plate": "DUP001",
        "monthly_cost_cents": 45000
    })
    
    # Intentar crear otro con la misma matrícula
    response = client.post("/vehicles/", json={
        "brand": "Honda",
        "model": "Civic",
        "year": 2024,
        "license_plate": "DUP001",
        "monthly_cost_cents": 50000
    })
    
    assert response.status_code == 400
    assert "matrícula ya existe" in response.json()["detail"]

def test_list_vehicles(client):
    """Test: Listar vehículos"""
    # Crear dos vehículos
    client.post("/vehicles/", json={
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2024,
        "license_plate": "LIST001",
        "monthly_cost_cents": 45000
    })
    client.post("/vehicles/", json={
        "brand": "Honda",
        "model": "Civic",
        "year": 2024,
        "license_plate": "LIST002",
        "monthly_cost_cents": 50000
    })
    
    response = client.get("/vehicles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
