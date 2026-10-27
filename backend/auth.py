
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash


# Carrega as variáveis do arquivo .env
load_dotenv()

# Configuração dos tokens JWT
SECRET_KEY = os.getenv("STUDYAI_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 30

if not SECRET_KEY:
    raise RuntimeError(
        "Configure STUDYAI_SECRET_KEY no arquivo .env"
    )


# Configuração do hash de senhas
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Gera um hash seguro para armazenar a senha."""
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    """Verifica a senha informada contra o hash armazenado."""
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: int) -> str:
    """Cria um token JWT com validade de 30 minutos."""
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
