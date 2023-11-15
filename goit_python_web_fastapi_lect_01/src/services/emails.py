from pathlib import Path
from os import environ
from dotenv import load_dotenv

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
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


if not environ.get("MAIL_USERNAME"):
    load_dotenv()

assert environ.get("MAIL_USERNAME") is not None, "Check ENVIROMENTS of file .env"

conf = ConnectionConfig(
    MAIL_USERNAME=environ.get("MAIL_USERNAME", ""),
    MAIL_PASSWORD=environ.get("MAIL_PASSWORD", ""),
    MAIL_FROM=environ.get("MAIL_FROM", environ.get("MAIL_USERNAME", "")),
    MAIL_PORT=int(environ.get("MAIL_PORT", 465)),
    MAIL_SERVER=environ.get("MAIL_SERVER", ""),
    MAIL_FROM_NAME=environ.get("MAIL_USERNAME", ""),
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)
