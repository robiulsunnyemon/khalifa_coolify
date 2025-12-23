from fastapi_mail import FastMail,MessageSchema,ConnectionConfig,MessageType
from app.schemas.send_otp import SendOtpModel
import os
from dotenv import load_dotenv


load_dotenv()


conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = int(os.getenv("MAIL_PORT")),
    MAIL_SERVER = os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)



async def send_otp(send_otp_data: SendOtpModel):
    subject = "🔑 Your OTP Code"
    body = f"""
      <h3>Hello,</h3>
      <p>Your OTP code is: <b>{send_otp_data.otp}</b></p>
      <p>This code will expire in 5 minutes.</p>
      """

    message = MessageSchema(
        subject=subject,
        recipients=[send_otp_data.email],
        body=body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)