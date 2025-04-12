import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
DIRECT_URL="postgresql+asyncpg://postgres.mmiyafqvgmknxbqeepha:Edwin.4967%@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"

engine = create_async_engine(DIRECT_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()