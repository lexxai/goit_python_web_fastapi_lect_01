from pathlib import Path
from os import environ
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

from src.services.auth.auth import auth_service


class EmailSchema(BaseModel):
    email: EmailStr
    fullname: str = "Sender Name"
    subject: str = "Sender Subject topic"


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

app = FastAPI()

print(conf.MAIL_PASSWORD)


@app.post("/send-email")
async def send_email(background_tasks: BackgroundTasks, email: EmailSchema):
    try:       

        token_verification = auth_service.create_email_token({"sub:": email})

        message = MessageSchema(
            subject=body.subject,
            recipients=[body.email],
            template_body={"fullname": body.fullname},
            subtype=MessageType.html,
        )
        print(message)
        fm = FastMail(conf)

        background_tasks.add_task(
            fm.send_message, message, template_name="cats_email.html"
        )

    except:
        ...

    return {"message": "email has been set to sending query"}




@app.post("/send_in_background")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    try:       
        message = MessageSchema(
            subject=body.subject,
            recipients=[body.email],
            template_body={"fullname": body.fullname},
            subtype=MessageType.html,
        )
        print(message)
        fm = FastMail(conf)

        background_tasks.add_task(
            fm.send_message, message, template_name="cats_email.html"
        )

    except:
        ...

    return {"message": "email has been set to sending query"}


if __name__ == "__main__":
    uvicorn.run("emails:app", port=9090, reload=True)
