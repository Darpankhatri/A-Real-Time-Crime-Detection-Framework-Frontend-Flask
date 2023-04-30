import os
from dotenv import load_dotenv


load_dotenv()

class mailConfig:
    MAIL_SERVER= os.environ.get("MAIL_SERVER")
    MAIL_PORT= os.environ.get("MAIL_PORT")
    MAIL_USERNAME= os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD= os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    