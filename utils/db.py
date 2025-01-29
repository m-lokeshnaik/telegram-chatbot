# utils/db.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

async def get_db():
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    return client.telegram_bot