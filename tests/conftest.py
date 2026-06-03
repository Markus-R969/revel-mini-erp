import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_db
from app.main import app
from app.config import get_settings

# Usar una base de datos de prueba separada
TEST_DATABASE_URL = "postgresql://revel_user:revel_password@localhost:5432/revel_erp_test"

@pytest.fixture(scope="function")
def db_session():
    """Crear una sesión de base de datos para cada test"""
    engine = create_engine(TEST_DATABASE_URL)
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        # Limpiar la base de datos después de cada test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Crear un cliente de prueba para FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
