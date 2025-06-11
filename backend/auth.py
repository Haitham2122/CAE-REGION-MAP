from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "mon_secret_super_sécurisé"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#DOMAIN="https://mon-domaine.com"

from starlette.requests import Request

def generate_reset_link(request: Request, reset_token: str) -> str:
    """Génère dynamiquement le lien de réinitialisation basé sur la requête HTTP."""
    base_url = str(request.base_url).rstrip("/")  # Récupère le domaine automatiquement
    return f"{base_url}/reset-password?token={reset_token}"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
