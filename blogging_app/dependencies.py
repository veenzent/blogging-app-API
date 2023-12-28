import random
import smtplib, ssl
from email.message import EmailMessage
from instance.config import EMAIL_PASSWORD
from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_otp(length: int = 6) -> int:
    return " ".join([str(random.randint(0, 9)) for _ in range(length)])

def send_mail(email_receiver: str, email_subject: str, email_body):
    email_sender = "antisocialdev23@gmail.com"
    email_password = EMAIL_PASSWORD

    msg = EmailMessage()
    msg['Subject'] = email_subject
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg.set_content(email_body)
    print(f"the type of msg is: {type(msg)}")
    print(f"the type of msg is: {type(msg)}")
    print(f"msg: {msg}")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_sender, email_password)
        server.send_message(msg, email_sender, email_receiver)
        # server.send_message(msg)
