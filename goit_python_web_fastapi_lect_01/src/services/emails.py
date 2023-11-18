from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel

from src.conf.config import settings
from src.services.auth.auth import auth_service


class EmailSchema(BaseModel):
    email: EmailStr
    fullname: str = "Sender Name"
    subject: str = "Sender Subject topic"


async def send_email(email: str, username: str, host: str):
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={
                "token": token_verification,
                "host": host,
                "username": username,
            },
            subtype=MessageType.html,
        )
        print(message)

        fm = FastMail(conf)
        await fm.send_message(message, template_name="confirm_email.html")
    except ConnectionError as err:
        print(err)
        return None
    return {"message": "email has been set to sending query"}


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)
