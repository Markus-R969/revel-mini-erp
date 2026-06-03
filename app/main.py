from fastapi import FastAPI
from app.routers import vehicles, customers, contracts, payments

app = FastAPI(
    title="Mini-ERP de Flota de Vehículos",
    description="API para gestionar flota, contratos de renting y cobros. Inspirado en REVEL.",
    version="1.0.0"
)

# Registrar routers
app.include_router(vehicles.router)
app.include_router(customers.router)
app.include_router(contracts.router)
app.include_router(payments.router)

@app.get("/")
def root():
    return {
        "message": "Mini-ERP de Flota REVEL",
        "docs": "/docs",
        "status": "running"
    }
