from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from database import User as us
from database import Database as db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
csrf = CSRFProtect(app)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

@app.route('/', methods=['GET', 'POST'])
def anmelden():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if not username or not password:
            return 'Please fill all the fields'
        user = us().check_nm_pwd(username, password)
        if user:
            return render_template("index.html")
    return render_template('anmelden.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if not username or not password:
            return 'Please fill all the fields'
        user = us().get_user(username)
        if user:
            return 'User already exists'
        if not us().check_password_strength(password):
            return 'Password is too weak (12 characters required)\n your request has been denied'
        us().add_user(username, password)
        return 'User registered'
    return render_template('register.html', form=form)

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)