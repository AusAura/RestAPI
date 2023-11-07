from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from fastapi_mail.errors import ConnectionErrors

from src.services.auth import auth_service
from src.conf.config import settings

from icecream import ic


class EmailSchema(BaseModel):
    email: EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Verification email for Contact_sss",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

fm = FastMail(conf)

async def send_verification(body: str, username: str) -> bool:
    """
    Generates email token for the user, then makes email with it, passes the data to the template. At the end, sends a verification letter to the user's email.

    :param body: The email address of the user.
    :type body: str
    :param db:
    :type db: Session
    :rtype: bool
    """
    try:
        email_token = await auth_service.create_email_token({'sub': body})
        message = MessageSchema(
            subject="Fastapi mail module",
            recipients=[ic(body)],
            template_body={"email": body, "email_token": email_token, "username": username},
            subtype=MessageType.html
        )
        ic(email_token)

        await fm.send_message(message, template_name="example_email.html")
            # background_tasks.add_task(fm.send_message, message, template_name="example_email.html")
        return True
    
    except ConnectionErrors as err:
        ic(err)
    except Exception as e:
        ic(e)


async def send_reset(email: str, username: str) -> str:
    """
    Generates mew password for the user. Sends email to his email address with the new password.

    :param email: The email address of the user.
    :type email: str
    :param username: The username.
    :type username: str
    :rtype: bool
    """
    try:
        email_token = await auth_service.create_email_token({'sub': email})
        email_token = email_token[-13]
        ic(email_token)

        message = MessageSchema(
            subject="Reset email from Contact_sss",
            recipients=[ic(email)],
            template_body={"email": email, "email_token": email_token, "username": username},
            subtype=MessageType.html
        )

        await fm.send_message(message, template_name="reset_email.html")
            # background_tasks.add_task(fm.send_message, message, template_name="example_email.html")
        return email_token
    
    except ConnectionErrors as err:
        ic(err)
    except Exception as e:
        ic(e)