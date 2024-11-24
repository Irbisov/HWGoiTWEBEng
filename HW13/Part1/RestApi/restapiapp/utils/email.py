import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config import settings


async def send_reset_password_email(email: str, reset_token: str):
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"  # URL на фронтенді
    subject = "Password Reset Request"

    # Формування тіла листа
    html_content = f"""
    <html>
        <body>
            <h2>Password Reset</h2>
            <p>You requested to reset your password. Click the link below to proceed:</p>
            <a href="{reset_url}">Reset Password</a>
            <p>If you did not request this, please ignore this email.</p>
        </body>
    </html>
    """

    # Налаштування MIME
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = email

    part = MIMEText(html_content, "html")
    message.attach(part)

    # Відправка листа через SMTP
    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM_EMAIL, email, message.as_string())
        print(f"Password reset email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise
