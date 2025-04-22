from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="app/.env")
DIRECT_URL = os.getenv("DIRECT_URL")
print(f"Connecting to database at {DIRECT_URL}")

engine = create_async_engine(DIRECT_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
