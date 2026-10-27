
import re
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated
import hashlib
import secrets

from datetime import datetime, timedelta, timezone

from models import PasswordResetToken
from email_service import send_password_reset_email
import jwt
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)


# =========================================================
# CONFIGURACAO
# =========================================================

security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="StudyAI API",
    description="Backend do aplicativo de estudos com IA",
    version="0.4.0",
    lifespan=lifespan,
)


# =========================================================
# MODELOS DAS REQUISICOES
# =========================================================

class RegisterRequest(BaseModel):
    display_name: str = Field(
        min_length=2,
        max_length=100,
    )
    email: str = Field(
        min_length=5,
        max_length=254,
    )
    password: str = Field(
        min_length=8,
        max_length=128,
    )

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 2:
            raise ValueError("Informe um nome válido.")

        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()

        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.fullmatch(pattern, value):
            raise ValueError("Informe um e-mail válido.")

        return value


class LoginRequest(BaseModel):
    email: str = Field(
        min_length=5,
        max_length=254,
    )
    password: str = Field(
        min_length=1,
        max_length=128,
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(
        min_length=1,
        max_length=128,
    )
    new_password: str = Field(
        min_length=8,
        max_length=128,
    )


class PasswordResetRequest(BaseModel):
    email: str = Field(
        min_length=5,
        max_length=254,
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        value = value.strip().lower()

        if not re.fullmatch(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            value,
        ):
            raise ValueError("Informe um e-mail válido.")

        return value


class PasswordResetConfirmRequest(BaseModel):
    token: str = Field(
        min_length=20,
        max_length=200,
    )
    new_password: str = Field(
        min_length=8,
        max_length=128,
    )



# =========================================================
# AUTENTICACAO JWT
# =========================================================

def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    invalid_token = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        subject = payload.get("sub")

        if not subject:
            raise invalid_token

        user_id = int(subject)

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise invalid_token

    user = db.get(User, user_id)

    if user is None or not user.is_active:
        raise invalid_token

    return user


# =========================================================
# ROTAS PUBLICAS
# =========================================================

@app.get("/")
def home():
    return {
        "app": "StudyAI",
        "status": "online",
        "message": "Backend iniciado com sucesso!",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "ai": "not_connected",
    }


# =========================================================
# CADASTRO
# =========================================================

@app.post(
    "/auth/register",
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
):
    existing_user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível cadastrar essa conta.",
        )

    user = User(
        display_name=data.display_name,
        email=data.email,
        password_hash=hash_password(data.password),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível cadastrar essa conta.",
        )

    return {
        "message": "Conta criada com sucesso!",
        "user": {
            "id": user.id,
            "display_name": user.display_name,
            "email": user.email,
        },
    }


# =========================================================
# LOGIN
# =========================================================

@app.post("/auth/login")
def login(
    data: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
):
    user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if (
        user is None
        or not user.is_active
        or not verify_password(
            data.password,
            user.password_hash,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 1800,
    }


# =========================================================
# CONSULTAR CONTA AUTENTICADA
# =========================================================

@app.get("/auth/me")
def get_my_account(
    user: Annotated[User, Depends(get_current_user)],
):
    return {
        "id": user.id,
        "display_name": user.display_name,
        "email": user.email,
    }


# =========================================================
# ALTERAR SENHA
# =========================================================

@app.post("/auth/change-password")
def change_password(
    data: ChangePasswordRequest,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    # Confirma a identidade usando a senha atual.
    if not verify_password(
        data.current_password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta.",
        )

    # Impede uma alteracao sem efeito.
    if data.current_password == data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A nova senha deve ser diferente da atual.",
        )

    # Armazena somente o hash da nova senha.
    user.password_hash = hash_password(data.new_password)

    try:
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível alterar a senha.",
        )

    return {
        "message": "Senha alterada com sucesso!"
    }

# =========================================================
# RECUPERAR SENHA
# =========================================================

@app.post("/auth/forgot-password")
def forgot_password(
    request: PasswordResetRequest,
    db: Annotated[Session, Depends(get_db)],
):
    # A resposta não revela se o e-mail está cadastrado.
    generic_response = {
        "message": (
            "Se o e-mail estiver cadastrado, "
            "você receberá instruções para recuperar a senha."
        )
    }

    user = db.scalar(
        select(User).where(User.email == request.email)
    )

    if user is None or not user.is_active:
        return generic_response

    now = datetime.now(timezone.utc)

    # Invalida tokens anteriores ainda não utilizados.
    old_tokens = db.scalars(
        select(PasswordResetToken).where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        )
    ).all()

    for old_token in old_tokens:
        old_token.used_at = now

    # O token original só será enviado por e-mail.
    raw_token = secrets.token_urlsafe(32)

    token_record = PasswordResetToken(
        user_id=user.id,
        token_hash=hashlib.sha256(
            raw_token.encode("utf-8")
        ).hexdigest(),
        expires_at=now + timedelta(minutes=15),
    )

    db.add(token_record)
    db.commit()

    try:
        send_password_reset_email(
            recipient=user.email,
            reset_token=raw_token,
        )
    except Exception as exc:
        # Detalhes somente no terminal do backend.
        print(f"Falha ao enviar e-mail de recuperação: {exc}")

        token_record.used_at = datetime.now(timezone.utc)
        db.commit()

    return generic_response


@app.post("/auth/reset-password")
def reset_password(
    request: PasswordResetConfirmRequest,
    db: Annotated[Session, Depends(get_db)],
):
    token_hash = hashlib.sha256(
        request.token.encode("utf-8")
    ).hexdigest()

    token_record = db.scalar(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash
        )
    )

    if token_record is None or token_record.used_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado.",
        )

    now = datetime.now(timezone.utc)
    expires_at = token_record.expires_at

    # SQLite pode devolver datas sem informação de fuso horário.
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= now:
        token_record.used_at = now
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado.",
        )

    user = db.get(User, token_record.user_id)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado.",
        )

    user.password_hash = hash_password(request.new_password)
    token_record.used_at = now

    # Invalida todos os outros tokens pendentes desse usuário.
    other_tokens = db.scalars(
        select(PasswordResetToken).where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.id != token_record.id,
            PasswordResetToken.used_at.is_(None),
        )
    ).all()

    for other_token in other_tokens:
        other_token.used_at = now

    db.commit()

    return {
        "message": "Senha redefinida com sucesso."
    }
