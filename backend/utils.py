from passlib.context import CryptContext
import jwt
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from backend.auth import SECRET_KEY, ALGORITHM

# Create a hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain text password before storing it."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a given plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def generate_reset_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.now() + timedelta(hours=1/60)  # Token valid for 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Send Reset Email
def send_reset_email(to_email: str, reset_link: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"

    subject = "🔒 Réinitialisation de votre mot de passe"
    body = f"Bonjour,\n\nCliquez sur le lien suivant pour réinitialiser votre mot de passe : {reset_link}\n\nCe lien expirera dans 1 heure."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
    except Exception as e:
        print("Erreur lors de l'envoi de l'email :", e)
