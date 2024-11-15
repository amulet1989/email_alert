import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from app.config import SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD


def send_email_alert(emails, frame_path):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(
        emails
    )  # Agregar todos los destinatarios en un solo encabezado "To"
    msg["Subject"] = "Alerta de Robo"
    msg.attach(
        MIMEText(
            "Se ha detectado una alerta de robo. Adjunto el frame capturado.", "plain"
        )
    )

    # Adjuntar el frame capturado
    with open(frame_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={frame_path}")
        msg.attach(part)

    # Enviar el email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(
            EMAIL_USER, emails, msg.as_string()
        )  # Enviar el email a todos los destinatarios
    print(f"Email enviado a: {', '.join(emails)}")
