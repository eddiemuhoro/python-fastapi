from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, SessionLocal
from .models import Base
from .crud import get_all_devices, get_all_discharge_data

# This runs once when the server starts
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # Runs the SQL to create tables from your models if they don't already exist
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/devices")
async def read_devices():
    devices = await get_all_devices(db=SessionLocal())
    return devices

@app.get("/discharge_data")
async def read_discharge_data():
    discharge_data = await get_all_discharge_data(db=SessionLocal())
    return discharge_data