
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"A variável {name} não está configurada no .env"
        )

    return value


def send_password_reset_email(
    recipient: str,
    reset_token: str,
) -> None:
    smtp_host = get_required_env("SMTP_HOST")
    app_url = get_required_env("STUDYAI_APP_URL")

    try:
        smtp_port = int(os.getenv("SMTP_PORT", "25"))
    except ValueError as exc:
        raise RuntimeError(
            "SMTP_PORT precisa ser um número válido."
        ) from exc

    smtp_user = os.getenv("SMTP_USER", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    use_tls = (
        os.getenv("SMTP_USE_TLS", "false").strip().lower()
        in ("1", "true", "yes", "sim")
    )

    if bool(smtp_user) != bool(smtp_password):
        raise RuntimeError(
            "Configure SMTP_USER e SMTP_PASSWORD juntos."
        )

    sender = os.getenv(
        "STUDYAI_FROM_EMAIL",
        "studyai@localhost",
    )

    reset_link = (
        f"{app_url.rstrip('/')}/reset-password"
        f"?token={reset_token}"
    )

    message = EmailMessage()
    message["Subject"] = "Recuperação de senha - StudyAI"
    message["From"] = sender
    message["To"] = recipient

    message.set_content(
        "Você solicitou a recuperação da senha do StudyAI.\n\n"
        f"Acesse este link para redefinir sua senha:\n{reset_link}\n\n"
        "O link expira em 15 minutos e só pode ser usado uma vez.\n"
        "Se você não solicitou a recuperação, ignore este e-mail."
    )

    with smtplib.SMTP(
        smtp_host,
        smtp_port,
        timeout=15,
    ) as server:
        if use_tls:
            server.starttls()

        if smtp_user and smtp_password:
            server.login(smtp_user, smtp_password)

        server.send_message(message)
