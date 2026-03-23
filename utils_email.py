import smtplib
from email.message import EmailMessage
from config import Config

def send_email(to_email, subject, body):
    # If no credentials provided, just print to console (safe for demo)
    if not Config.MAIL_USERNAME or not Config.MAIL_PASSWORD:
        print(f"[EMAIL SIM] To: {to_email}\nSubject: {subject}\n{body}\n")
        return True

    msg = EmailMessage()
    msg["From"] = Config.ALERT_EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as smtp:
            smtp.starttls()
            smtp.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False


# Test block to send a test email when running this file directly
if __name__ == "__main__":
    result = send_email(
        "eswarigeetha2005@gmail.com",
        "Test Email from MediTracker",
        "This is a test email to verify your email sending setup."
    )
    if result:
        print("Test email sent successfully.")
    else:
        print("Test email failed to send.")
