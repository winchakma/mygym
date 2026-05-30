import asyncio
from httpx import AsyncClient
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from backend.main import app
from backend.app.database import init_db

async def test_live_feed():
    await init_db()
    from httpx import ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/user/chat-brain", json={"message": "I am 80kg 180cm and want to lose weight"})
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        try:
            print(response.json())
        except:
            print(response.text)

if __name__ == "__main__":
    asyncio.run(test_live_feed())
