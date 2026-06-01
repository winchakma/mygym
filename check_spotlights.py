import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def run():
    client = AsyncIOMotorClient('mongodb+srv://winchakma:b2N3J34vL2l21bVq@cluster0.aigw1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    db = client.get_database('test')
    docs = await db.get_collection('community_spotlights').find().to_list(100)
    for d in docs:
        print(d)

asyncio.run(run())
