from fastapi_mail import ConnectionConfig
import os
from pydantic import SecretStr
from dotenv import load_dotenv
from typing import cast

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=cast(str, os.getenv("MAIL_USERNAME")),
    MAIL_PASSWORD=SecretStr(cast(str, os.getenv("MAIL_PASSWORD"))),
    MAIL_FROM=cast(str, os.getenv("MAIL_FROM")),
    MAIL_PORT=587,
    MAIL_SERVER=cast(str, os.getenv("MAIL_SERVER")),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)