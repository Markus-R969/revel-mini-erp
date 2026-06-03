# Mini-ERP de Flota de Vehículos

Sistema backend para gestionar flota de vehículos, contratos de renting y cobros mensuales. Diseñado como simulador del sistema operativo interno de una empresa de renting como **REVEL**.

## 🎯 Problema que resuelve

REVEL gestiona miles de contratos de renting con cobros mensuales automáticos. Este proyecto replica los conceptos clave:

- **Fuente de la verdad operativa**: PostgreSQL como registro central de flota, contratos y pagos
- **Transacciones atómicas**: Crear contrato + cambiar estado del vehículo + generar pago en una sola operación
- **Idempotencia**: Protección contra cobros duplicados si Stripe reenvía webhooks
- **Integraciones con terceros**: Campo \stripe_payment_id\ preparado para webhooks de Stripe
- **Validaciones de negocio**: No alquilar vehículos ocupados, fechas coherentes, matrículas únicas

## 🏗️ Arquitectura

\\\
┌─────────────┐
│  FastAPI    │  ← API REST con validaciones
└──────┬──────┘
       │
┌──────▼──────┐
│ PostgreSQL  │  ← Fuente de la verdad operativa
└─────────────┘
       │
┌──────▼──────┐
│  Stripe     │  ← Integración de pagos (preparada)
└─────────────┘
\\\

### Modelo de datos

- **Vehicle**: Flota de vehículos con estado (AVAILABLE, RENTED, MAINTENANCE, RETIRED)
- **Customer**: Clientes con datos fiscales
- **Contract**: Contratos de renting con fechas, cuotas y próximo cobro
- **Payment**: Pagos mensuales con idempotencia vía \stripe_payment_id\

## 🚀 Cómo levantarlo

### 1. Clonar el repositorio
\\\ash
git clone https://github.com/TU_USUARIO/revel-mini-erp.git
cd revel-mini-erp
\\\

### 2. Levantar PostgreSQL con Docker
\\\ash
docker-compose up -d
\\\

### 3. Crear entorno virtual e instalar dependencias
\\\ash
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
\\\

### 4. Crear tablas en la base de datos
\\\ash
python test_db.py
\\\

### 5. Levantar la API
\\\ash
uvicorn app.main:app --reload
\\\

La API estará disponible en \http://127.0.0.1:8000\  
Documentación interactiva (Swagger UI) en \http://127.0.0.1:8000/docs\

## 🧪 Tests automatizados

\\\ash
pytest tests/ -v
\\\

### Cobertura de tests

| Test | Qué demuestra |
|---|---|
| \	est_create_vehicle\ | API funciona correctamente |
| \	est_create_vehicle_duplicate_plate\ | Validación: matrículas únicas |
| \	est_create_contract_success\ | **Transacción atómica**: contrato + vehículo RENTED + pago PENDING |
| \	est_create_contract_vehicle_not_available\ | Validación: no alquilar vehículo ocupado |
| \	est_create_contract_invalid_dates\ | Validación: fechas coherentes |
| \	est_payment_idempotency\ | **Idempotencia**: no procesar el mismo pago dos veces |
| \	est_mark_payment_not_found\ | Manejo de errores: recursos inexistentes |

## 📚 Decisiones técnicas

### 1. Dinero en céntimos (Integer), no en euros (Float)
**Problema**: Los floats tienen errores de redondeo (0.1 + 0.2 ≠ 0.3 en binario).  
**Solución**: Guardar 450.00€ como 45000 céntimos (Integer).  
**Beneficio**: Cálculos exactos, sin errores de redondeo en cobros masivos.

### 2. UUID como primary key
**Problema**: IDs auto-incrementales revelan cuántos registros tienes y son predecibles.  
**Solución**: UUIDs v4 como primary keys.  
**Beneficio**: Seguridad (no revela volumen de negocio), mejor para APIs distribuidas.

### 3. Transacciones atómicas en creación de contratos
**Problema**: Si fallas después de crear el contrato pero antes de cambiar el estado del vehículo, tienes datos inconsistentes.  
**Solución**: Todo en una transacción con \db.flush()\ y \db.commit()\.  
**Beneficio**: O todo funciona o nada se guarda. Integridad de datos garantizada.

### 4. Idempotencia en pagos con \stripe_payment_id\
**Problema**: Stripe puede enviar el mismo webhook dos veces (retry automático). Sin idempotencia, cobrarías dos veces.  
**Solución**: Campo \stripe_payment_id\ con \unique=True\. Si Stripe reenvía el webhook, la base de datos rechaza el duplicado.  
**Beneficio**: Protección contra cobros duplicados, crítico en sistemas de pagos.

### 5. Validaciones de negocio en el backend
**Problema**: Un cliente podría alquilar un vehículo que ya está alquilado si solo validas en el frontend.  
**Solución**: Validaciones en el endpoint \POST /contracts/\: verificar que el vehículo está AVAILABLE antes de crear el contrato.  
**Beneficio**: Integridad de datos incluso si alguien usa la API directamente (sin frontend).

## 🔌 Endpoints principales

### Vehicles
- \POST /vehicles/\ - Crear vehículo
- \GET /vehicles/\ - Listar vehículos (filtro por status)
- \GET /vehicles/{id}\ - Detalle de vehículo

### Customers
- \POST /customers/\ - Crear cliente
- \GET /customers/\ - Listar clientes
- \GET /customers/{id}\ - Detalle de cliente

### Contracts
- \POST /contracts/\ - Crear contrato (transacción atómica)
- \GET /contracts/\ - Listar contratos
- \GET /contracts/{id}\ - Detalle de contrato

### Payments
- \GET /payments/\ - Listar pagos (filtro por status)
- \POST /payments/{id}/mark-paid\ - Marcar como pagado (idempotente)

## 🚧 Próximos pasos

- [ ] Integración real con Stripe (webhooks)
- [ ] Cola de trabajos con Celery + Redis para generación masiva de cobros mensuales
- [ ] Dashboard frontend con React
- [ ] Sistema de autenticación y autorización (JWT)
- [ ] Monitoring con Prometheus + Grafana
- [ ] CI/CD con GitHub Actions

## 🛠️ Stack tecnológico

- **Backend**: Python 3.12 + FastAPI
- **Base de datos**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Validación**: Pydantic 2.0
- **Tests**: pytest
- **Contenedores**: Docker + Docker Compose

## 📄 Licencia

MIT

