import asyncio
from httpx import AsyncClient
from backend.main import app
from backend.app.database import init_db

async def test_live_feed():
    await init_db()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/user/chat-brain", json={"message": "I am 80kg 180cm and want to lose weight"})
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        try:
            print(response.json())
        except:
            print(response.text)

if __name__ == "__main__":
    asyncio.run(test_live_feed())
