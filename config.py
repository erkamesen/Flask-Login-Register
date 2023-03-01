from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()


SECRET_KEY = "thisisasecretkey"
SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
HCAPTCHA_ENABLED = True
HCAPTCHA_SITE_KEY = os.getenv("HCAPTCHA_SITE_KEY")
HCAPTCHA_SECRET_KEY = os.getenv("HCAPTCHA_SECRET_KEY")
PERMANENT_SESSION_LIFETIME =  timedelta(minutes=5)
