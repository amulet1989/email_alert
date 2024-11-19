import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from app.config import SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD


def send_email_alert(to_emails, attachment_path):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    from app.config import EMAIL_USER, EMAIL_PASSWORD

    subject = "Alerta de robo detectada"
    body = """
    <html>
    <body>
        <p><strong>Alerta de seguridad:</strong></p>
        <p>Se ha detectado un evento sospechoso en el sistema de videovigilancia.</p>
        <p>Por favor, revise el archivo adjunto para más detalles.</p>
        <br>
        <hr>
        <p><strong>Go2future Security Alert System</strong><br>
        This email is automatically generated by Go2future's security monitoring system. Please do not reply to this message.<br>
        <br>
        If you believe this email was sent in error or need assistance, contact our support team at <a href="mailto:support@go2future.com">support@go2future.com</a>.<br>
        <br>
        Confidentiality Notice: This message, including any attachments, is intended solely for the recipient and may contain confidential information. If you are not the intended recipient, please delete this email and notify us immediately.<br>
        <br>
        <a href="http://www.go2future.com">www.go2future.com</a> | Transforming Retail with AI-Powered Vision</p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    # Agrega el cuerpo del correo
    msg.attach(MIMEText(body, 'html'))

    # Adjunta el archivo
    attachment_name = attachment_path.split("/")[-1]
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={attachment_name}",
    )
    msg.attach(part)

    # Enviar el correo
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            for email in to_emails:
                server.sendmail(EMAIL_USER, email, msg.as_string())
        print(f"Email enviado a: {', '.join(to_emails)}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
