import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file 
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# SMTP configuration and creadentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Function to send email 
# Formats the email and sends it using SMTP
def send_email(recipient_email: str, subject: str, body: str) -> bool:
    """
    Send an email using configured SMTP credentials.
    Returns True on success, False on dry-run or error.
    """
    sender = EMAIL_ADDRESS
    password = EMAIL_PASSWORD

    if not sender or not password:
        # dry-run
        print("(Dry-run) Email contents:")
        print(f"From: {sender}")
        print(f"To: {recipient_email}")
        print(f"Subject: {subject}")
        print(body)
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender, password)
            server.sendmail(sender, [recipient_email], msg.as_string())

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False