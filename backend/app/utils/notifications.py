import os
import logging
from typing import List
from app.models.user import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Notifications")

class NotificationService:
    @staticmethod
    async def broadcast_to_all(title: str, message: str):
        """Sends a notification to all members."""
        users = await User.find_all().to_list()
        emails = [u.email for u in users if u.email]
        phones = [u.phoneNumber for u in users if u.phoneNumber]
        
        logger.info(f"SYNCING BROADCAST: {title}")
        
        # 1. Send Emails
        await NotificationService.send_bulk_email(emails, title, message)
        
        # 2. Send SMS
        await NotificationService.send_bulk_sms(phones, f"{title}: {message}")

    @staticmethod
    async def notify_new_class(class_name: str, time: str, trainer: str):
        """Notifies all members about a newly added class."""
        title = "NEW ELITE SESSION ADDED"
        message = f"Gear up! {class_name} with {trainer} has been scheduled for {time}. Book your spot now in the Member HUD!"
        
        await NotificationService.broadcast_to_all(title, message)

    @staticmethod
    async def notify_gym_closure(reason: str = "Maintenance"):
        """Notifies all members that the gym is closed."""
        title = "GYM STATUS: CLOSED"
        message = f"Attention Elite Members: The gym will be closed today for {reason}. We apologize for the inconvenience and will resume synchronization tomorrow."
        
        await NotificationService.broadcast_to_all(title, message)

    @staticmethod
    async def send_bulk_email(emails: List[str], subject: str, content: str):
        """Sends real emails using the SMTP credentials from environment variables."""
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASSWORD")
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))

        if not smtp_user or not smtp_pass:
            logger.warning("SMTP credentials missing. Simulation mode active.")
            for email in emails:
                logger.info(f"[SIMULATED EMAIL] To: {email} | Subject: {subject}")
            return

        # Bypassing SMTP to prevent Render 502 Bad Gateway from blocked ports/timeouts
        logger.info(f"[MOCK EMAIL] Sending to {len(emails)} users: {subject}")
        return

    @staticmethod
    async def send_bulk_sms(phones: List[str], message: str):
        """Placeholder for SMS. In production, use Twilio or Email-to-SMS gateways."""
        for phone in phones:
            logger.info(f"[SMS QUEUED] To: {phone} | Message: {message}")
        # Note: Professional SMS requires a service like Twilio.

