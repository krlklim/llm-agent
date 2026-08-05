import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email: str, subject: str, body: str) -> str:
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SMTP_SENDER_EMAIL")
    sender_password = os.getenv("SMTP_SENDER_PASSWORD")

    if not sender_email or not sender_password:
        return "Error: SMTP credentials (SMTP_SENDER_EMAIL / SMTP_SENDER_PASSWORD) are not configured in .env."

    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        is_html = bool(re.search(r"<[a-z][\s\S]*>", body, re.IGNORECASE))

        if is_html:
            msg.attach(MIMEText(body, 'html', 'utf-8'))
        else:
            html_version = f"<html><body><p>{body.replace(chr(10), '<br>')}</p></body></html>"
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_version, 'html', 'utf-8'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.close()

        return f"Email successfully sent to {to_email} with subject '{subject}'."
    except Exception as e:
        return f"Failed to send email to {to_email}. Error: {str(e)}"
