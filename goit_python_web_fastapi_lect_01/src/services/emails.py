from pathlib import Path
from os import environ
from dotenv import load_dotenv

load_dotenv()

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

from src.services.auth.auth import auth_service

class EmailSchema(BaseModel):
    email: EmailStr




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

app = FastAPI()


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[body.email],
        template_body={"fullname": "Billy Jones"},
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name="example_email.html")

    return {"message": "email has been sent"}


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)




