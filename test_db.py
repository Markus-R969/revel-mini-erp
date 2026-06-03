from app.db import engine, Base
from app.models import Vehicle, Customer, Contract, Payment

Base.metadata.create_all(bind=engine)
print("✅" \
" Todas las tablas creadas correctamente")
