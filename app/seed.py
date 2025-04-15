from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .database import SessionLocal
from .models import Alerts

async def seed_alerts():
    async with SessionLocal() as session:
        async with session.begin():
            # Check if the table already has data
            result = await session.execute(select(Alerts))
            existing_alerts = result.scalars().all()
            if existing_alerts:
                print("Alerts table already seeded.")
                return

            # Seed data
            alerts = [
                Alerts(
                    device_id=1,
                    level=5.5,
                    message="High water level detected",
                    alertType="Warning",
                    abstractor_name="John Doe",
                    abstractor_phone="1234567890",
                    catchment="Catchment A"
                ),
                Alerts(
                    device_id=2,
                    level=3.2,
                    message="Low water level detected",
                    alertType="Info",
                    abstractor_name="Jane Smith",
                    abstractor_phone="0987654321",
                    catchment="Catchment B"
                )
            ]

            session.add_all(alerts)
            print("Alerts table seeded successfully.")

# Run the seeding function
import asyncio
asyncio.run(seed_alerts())