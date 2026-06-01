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

        import asyncio

        def sync_send_emails(recipients: List[str], mail_subject: str, mail_content: str, host: str, port: int, user: str, password: str):
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            for recipient in recipients:
                recipient_clean = recipient.strip().lower()
                if not recipient_clean:
                    continue
                try:
                    msg = MIMEMultipart()
                    msg["From"] = user
                    msg["To"] = recipient_clean
                    msg["Subject"] = mail_subject
                    
                    mime_type = "html" if "<html" in mail_content.lower() or "<p" in mail_content.lower() or "<div" in mail_content.lower() else "plain"
                    msg.attach(MIMEText(mail_content, mime_type))

                    # Connect and send
                    server = smtplib.SMTP(host, port, timeout=10)
                    server.starttls()
                    server.login(user, password)
                    server.sendmail(user, recipient_clean, msg.as_string())
                    server.quit()
                    logger.info(f"[SMTP EMAIL SUCCESS] Delivered to: {recipient_clean}")
                except Exception as e:
                    logger.error(f"[SMTP EMAIL ERROR] Failed delivering to {recipient_clean}: {e}")

        # Offload blocking SMTP calls to a background thread to prevent Render HTTP request timeout (502 Bad Gateway)
        logger.info(f"[SMTP BACKGROUND INITIATED] Queued {len(emails)} emails: {subject}")
        asyncio.create_task(asyncio.to_thread(sync_send_emails, emails, subject, content, smtp_host, smtp_port, smtp_user, smtp_pass))

    @staticmethod
    async def send_bulk_sms(phones: List[str], message: str):
        """Placeholder for SMS. In production, use Twilio or Email-to-SMS gateways."""
        for phone in phones:
            logger.info(f"[SMS QUEUED] To: {phone} | Message: {message}")
        # Note: Professional SMS requires a service like Twilio.

