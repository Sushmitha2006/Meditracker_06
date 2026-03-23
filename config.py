import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "meditracker.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # For email notifications (optional) - change to your SMTP if you want real emails
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "eswarigeetha2005@gmail.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "adrsfovotqhetfqm")
    MAIL_USE_TLS = True
    ALERT_EMAIL_FROM = os.environ.get("ALERT_EMAIL_FROM", "no-reply@meditracker.local")
