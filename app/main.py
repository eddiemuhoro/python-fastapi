from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, SessionLocal
from .models import Base
from .crud import get_all_devices, get_all_discharge_data, get_all_alerts, get_all_conversations_by_user, get_latest_conversation_by_user, get_messages_by_conversation
from .chat import router as chat_router

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

@app.get("/api/conversations/query")
async def fetch_conversations(
    user_id: str = Query(...),
    latest: bool = Query(False),
    db: AsyncSession = Depends(get_db)
):
    if latest:
        conversation = await get_latest_conversation_by_user(db, user_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="No conversation found.")
        return {
            "id": conversation.id,
            "user_id": conversation.user_id,
            "created_at": conversation.created_at
        }

    conversations = await get_all_conversations_by_user(db, user_id)
    return [
        {"id": c.id, "user_id": c.user_id, "created_at": c.created_at}
        for c in conversations
    ]

@app.get("/api/chat/{conversation_id}/history")
async def get_chat_history(conversation_id: int, db: AsyncSession = Depends(get_db)):
    messages = await get_messages_by_conversation(db, conversation_id)
    return [
        {"role": msg.role, "content": msg.content, "timestamp": msg.timestamp}
        for msg in messages
    ]


app.include_router(chat_router)