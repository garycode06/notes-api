from fastapi_mail import MessageSchema, MessageType, NameEmail, FastMail
from typing import cast
from dotenv import load_dotenv
import os
from app.core.mail_config import conf

load_dotenv()

def config_message(dest: str):
    message = MessageSchema(
        subject="Inscription sur NoteVault",
        recipients=cast(list[NameEmail], [dest]),
        reply_to=cast(list[NameEmail], [cast(str, os.getenv("MAIL_FROM"))]),
        body="<h1>Votre inscription a été validé avec succès !</h1>",
        subtype=MessageType.html,
    )
    return message

async def send_email(dest: str):
    fm = FastMail(conf)       # conf est votre ConnectionConfig
    await fm.send_message(config_message(dest))