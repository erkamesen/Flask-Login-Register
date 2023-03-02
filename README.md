# Flask-Login-Register
Flask Login&amp;Register Example with hCaptcha and Activation Code 


## Features
a sample application made for users to register and login
- Users can be register and login
- For registration, all users must successfully enter the 6-digit activation code sent by e-mail.
- Users must successfully pass hCaptcha verification to login.
- Basically in model.py there is a simple sqlalchemy table(User) which is required for user login and other processes.


## Install and Usage
- Clone to the repository
```
git clone https://github.com/erkamesen/Flask-Login-Register.git
```
- Navigate to app
```
cd Flask-Login-Register
```
- Install requirements
```
pip install -r requirements.txt
```
- Set hCaptcha and SMTP tokens
- Run server
```
flask run
```
Now Flask-Login-Register app running on your localhost - http://127.0.0.1:5000

## User Table Model with SQLAlchemy

models.py
```
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
```


# Python Files

## Config

config.py
```
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
```
set HCAPTCHA_SITE_KEY & HCAPTHCA_SECRET_KEY with your own Tokens !

## Forms with Flask_wtf

forms.py
```
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    name = StringField("Your Name:",
                        validators=[DataRequired()])
    email = EmailField("Your Email:",
                        validators=[DataRequired()])
    password = PasswordField("Password:",
                        validators=[DataRequired()])
    submit = SubmitField("Register")



class LoginForm(FlaskForm):
    email = EmailField("Your Email:",
                        validators=[DataRequired()])
    password = PasswordField("Password:",
                        validators=[DataRequired()])
    submit = SubmitField("Register")
```

## Mail Sender - smtplib 

mail_sender.py
```
from smtplib import SMTP




class MailSender:
    
    def __init__(self, token, sender_mail, 
                 mail_server="smtp.gmail.com", port=587):
        
        self.token = token
        self.sender_mail = sender_mail
        self.mail_server = mail_server
        self.port = port
        
    def send_password_link(self, receiver, link):
            with SMTP(self.mail_server, self.port) as connection:  
                connection.starttls()  
                connection.login(self.sender_mail, password=self.token)  
                connection.sendmail(from_addr=self.sender_mail,
                                                to_addrs=receiver,
                                                msg=f"Subject:Reset Password!\n\nYou can reset your password by following the link below:\n\n{link}")
    
    def send_activation_code(self, receiver, code):
            with SMTP(self.mail_server, self.port) as connection:  
                connection.starttls()  
                connection.login(self.sender_mail, password=self.token)  
                connection.sendmail(from_addr=self.sender_mail,
                                                to_addrs=receiver,
                                                msg=f"Subject:Activation Code!\n\nYou can complete your registration with the 6 digit code below:\n\n{code}")
    
```


## Utils

utils.py
```
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
    
```

set EMAIL and SMTPToken !!!


## Routes

app.py
```
from flask_bootstrap import Bootstrap
from forms import RegisterForm, LoginForm
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_hcaptcha import hCaptcha
from flask_login import LoginManager, login_required, login_user
from utils import make_activation_code, check_activation_code


app = Flask(__name__)
app.config.from_pyfile("config.py")



bs = Bootstrap(app)
db.init_app(app)
hcaptcha = hCaptcha(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    
    form = LoginForm()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        query_user = User.query.filter_by(email=email).first()
        if query_user:
            if hcaptcha.verify():
                if check_password_hash(query_user.password, password):
                    login_user(query_user)
                    return redirect(url_for("succes"))
                else:
                    flash("Email or password is wrong please check !")
                    return render_template("login.html")
            else:
                flash("Please verify hCaptcha")
                return render_template("login.html")
        else:
            flash("email does not exists, please register")
            return render_template("login.html")
    else:
        return render_template("login.html", form=form, hc=hcaptcha.get_code())

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    is_activation = True
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"))
        check_user = User.query.filter_by(email=email).first()
        if check_user:
            flash("email is already exists, try login or different email")
            return render_template("register.html")
        else:
            make_activation_code(email=email, name=name, password=password)
            return render_template("register.html", is_activation=is_activation, email = email)
    else:
        return render_template("register.html", form=form)


@app.route("/activation", methods=["POST"])
def activation():
    if request.method == "POST":
        code = request.form.get("activation_code")
        email = request.form.get("email")
        ses = session[email]
        if check_activation_code(email=email, code=code):
            name = ses["name"]
            password = ses["password"]
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit() 
            return redirect(url_for("login"))
        else:
            flash("Activation code is wrong!")
            return render_template("register.html")        
    


@app.route("/succes")
@login_required
def succes():
    return render_template("succes.html")



if __name__ == '__main__':
    app.run(debug=True)
```
