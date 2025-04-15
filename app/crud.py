from sqlalchemy.ext.asyncio import AsyncSession
from .models import Deployments, DischargeData, Alerts
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