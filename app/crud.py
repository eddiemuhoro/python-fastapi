from sqlalchemy.ext.asyncio import AsyncSession
from .models import Deployments, DischargeData, Alerts, Conversation, Message
from .database import SessionLocal
from sqlalchemy.future import select

async def get_all_devices(db: AsyncSession):
    result = await db.execute(select(Deployments))
    devices = result.scalars().all()
    return devices

async def get_all_discharge_data(db: AsyncSession):
    result = await db.execute(select(DischargeData))
    discharge_data = result.scalars().all()
    return discharge_data

async def get_all_alerts(db: AsyncSession):
    result = await db.execute(select(Alerts))
    alerts = result.scalars().all()
    return alerts

async def create_conversation(db: AsyncSession, user_id: str):
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation

async def get_conversation(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .limit(1)
    )
    return result.scalars().first()

async def create_message(db: AsyncSession, conversation_id: int, role: str, content: str):
    message = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message

async def get_messages_by_conversation(db: AsyncSession, conversation_id: int):
    result = await db.execute(
        select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp)
    )
    return result.scalars().all()

async def create_message(db: AsyncSession, conversation_id: int, role: str, content: str):
    message = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message

async def get_all_conversations_by_user(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
    )
    return result.scalars().all()

async def get_latest_conversation_by_user(db: AsyncSession, user_id: str):
    conversations = await get_all_conversations_by_user(db, user_id)
    return conversations[0] if conversations else None