import os
from pusher import Pusher
from dotenv import load_dotenv


load_dotenv()

class mailConfig:
    MAIL_SERVER= os.environ.get("MAIL_SERVER")
    MAIL_PORT= os.environ.get("MAIL_PORT")
    MAIL_USERNAME= os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD= os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False


class pusharConfig:
    pusher_client = Pusher(
        app_id = os.environ.get("Pusher_app_id"),
        key = os.environ.get("Pusher_key"),
        secret = os.environ.get("Pusher_secret"),
        cluster = os.environ.get("Pusher_cluster"),
        ssl = True
    )