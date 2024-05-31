import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    ROOT_LINK=os.getenv("ROOT_LINK")

    SECRET_KEY=os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")

    MAIL_SERVER="smtp.taskin-logistics.com"
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER")