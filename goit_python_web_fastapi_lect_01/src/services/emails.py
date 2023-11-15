from pathlib import Path
from os import environ
from dotenv import load_dotenv



from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth.auth import auth_service


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

print(conf.MAIL_USERNAME)




