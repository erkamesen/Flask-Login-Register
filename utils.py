from random import randint
import uuid
from flask import session
from mail_sender import MailSender
from dotenv import load_dotenv
import os
from flask import request

load_dotenv()

EMAIL = os.getenv("EMAIL")
SMTP_TOKEN = os.getenv("SMTP_TOKEN")

mail_sender = MailSender(token=SMTP_TOKEN, sender_mail=EMAIL)

def generate_code():
    code = randint(100000, 999999)
    return code



def make_activation_code(email, name, password):
    code = generate_code()
    mail_sender.send_activation_code(receiver=email, code=code)
    session[email]={"name":name,
                    "password":password,
                    f"{email}'s_activation_code":code}

    

def check_activation_code(code, email):
    ses = session[email]
    control = ses[f"{email}'s_activation_code"]
    if int(control) == int(code):
        return True
    else:
        return False
    


