
from email_service import send_password_reset_email

send_password_reset_email(
    recipient="teste@example.com",
    reset_token="token-de-teste",
)

print("E-mail de teste enviado ao smtp4dev!")
