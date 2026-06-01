import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import timedelta

async def run():
    client = AsyncIOMotorClient('mongodb+srv://winchakma:win123win@cluster0.htlsc44.mongodb.net/elite_gym?retryWrites=true&w=majority&appName=Cluster0')
    db = client.get_database('elite_gym')
    
    # Get all spotlights
    docs = await db.get_collection('community_spotlights').find().to_list(100)
    for doc in docs:
        print(f"Original activeFrom: {doc.get('activeFrom')}")
        
        # Subtract 6 hours to correct the UTC offset bug
        if 'activeFrom' in doc:
            new_from = doc['activeFrom'] - timedelta(hours=6)
            new_until = doc['activeUntil'] - timedelta(hours=6)
            
            await db.get_collection('community_spotlights').update_one(
                {'_id': doc['_id']},
                {'$set': {'activeFrom': new_from, 'activeUntil': new_until}}
            )
            print(f"Updated activeFrom to: {new_from}")

asyncio.run(run())
