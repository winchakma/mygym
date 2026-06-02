import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document
from datetime import datetime

class SupportMessage(Document):
    senderName: str
    senderEmail: str
    recipientType: str
    message: str
    reply: str = None
    status: str = "open"
    timestamp: datetime = datetime.utcnow()

    class Settings:
        name = "support_messages"

async def test():
    client = AsyncIOMotorClient("mongodb+srv://admin:admin123@cluster0.p7102.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    await init_beanie(database=client.mygym, document_models=[SupportMessage])
    
    msgs = await SupportMessage.find().sort("-timestamp").to_list()
    print("ALL MESSAGES IN DB:")
    for m in msgs:
        print(f"ID: {m.id} | From: {m.senderEmail} | To: {m.recipientType} | Msg: {m.message} | Reply: {m.reply}")
        
asyncio.run(test())
