from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
import os

# Load the .env file
load_dotenv()

smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))


def send_email(to_email, subject, body):
    if not to_email or "@" not in to_email or "." not in to_email.split("@")[-1]:
        raise ValueError("Invalid email address")
    if not body:
        raise ValueError("Message body cannot be empty")

    try:
        msg = EmailMessage()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        return {"status": "success", "message": f"Email successfully sent to {to_email}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
