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