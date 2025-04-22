from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, SessionLocal
from .models import Base
from .crud import get_all_devices, get_all_discharge_data, get_all_alerts, get_all_conversations_by_user, get_latest_conversation_by_user, get_messages_by_conversation
from .chat import router as chat_router
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# This runs once when the server starts
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # Runs the SQL to create tables from your models if they don't already exist
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/rdms/devices")
async def read_devices():
    devices = await get_all_devices(db=SessionLocal())
    return devices

@app.get("/rdms")
async def read_discharge_data():
    discharge_data = await get_all_discharge_data(db=SessionLocal())
    return discharge_data

@app.get("/alerts")
async def read_alerts():
    alerts = await get_all_alerts(db=SessionLocal())
    return alerts

@app.get("/api/conversations/query"+"/{user_id}")
async def get_conversations(user_id: str, db: AsyncSession = Depends(get_db)):
    conversations = await get_all_conversations_by_user(db, user_id)
    return [
        {"id": conv.id, "created_at": conv.created_at} for conv in conversations
    ]


app.include_router(chat_router)