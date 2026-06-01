import asyncio
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import init_db
from app.models.community import PrivateMessage

async def main():
    await init_db()
    messages = await PrivateMessage.find_all().to_list()
    print(f"Total messages: {len(messages)}")
    for m in messages:
        print(f"From: {m.senderEmail} -> To: {m.receiverEmail} | Msg: {m.message} | isRead: {m.isRead}")

if __name__ == "__main__":
    asyncio.run(main())
