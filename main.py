from fastapi import FastAPI
from address_app import models
from address_app.models import Base
from db.database import engine
from routers.address import router as address_router

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Include the address router
app.include_router(address_router)
