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