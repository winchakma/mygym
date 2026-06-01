import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def run():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['elite_gym']
    events = await db['community_events'].find().to_list(10)
    print("EVENTS:", events)

asyncio.run(run())
