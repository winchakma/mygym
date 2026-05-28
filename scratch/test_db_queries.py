import asyncio
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import init_db
from app.models.community import PrivateMessage, SocialProfile
from app.models.user import User

async def main():
    await init_db()
    
    print("Fetching private messages...")
    messages = await PrivateMessage.find_all().to_list()
    print(f"Total messages: {len(messages)}")
    
    print("Fetching users...")
    users = await User.find_all().to_list()
    print(f"Total users: {len(users)}")
    
    # Run the get_conversations logic for the first user
    if users:
        email = users[0].email.strip().lower()
        print(f"Testing get_conversations logic for user: {email}")
        
        sent = await PrivateMessage.find(PrivateMessage.senderEmail == email).to_list()
        received = await PrivateMessage.find(PrivateMessage.receiverEmail == email).to_list()
        
        partners = set()
        for m in sent: partners.add(m.receiverEmail)
        for m in received: partners.add(m.senderEmail)
        
        print(f"Found partners: {partners}")
        
        for p_email in partners:
            p_user = await User.find_one(User.email == p_email)
            if not p_user:
                print(f"Partner user not found in DB: {p_email}")
                continue
            
            last_msg = await PrivateMessage.find(
                ((PrivateMessage.senderEmail == email) & (PrivateMessage.receiverEmail == p_email)) |
                ((PrivateMessage.senderEmail == p_email) & (PrivateMessage.receiverEmail == email))
            ).sort("-timestamp").first_or_none()
            
            print(f"Partner {p_email}: Last Message: {last_msg.message if last_msg else 'None'}")

if __name__ == "__main__":
    asyncio.run(main())
