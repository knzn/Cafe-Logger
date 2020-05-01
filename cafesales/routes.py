from flask import render_template, url_for, flash, redirect
from cafesales import app, db, bcrypt
from cafesales.forms import RegistrationForm, LoginForm
from cafesales.models import User, Sale
from flask_login import login_user, current_user, logout_user, login_required

# sales = [
#     {
#         'amount': '3000',
#         'time_open': '9:30 AM',
#         'time_close': '4:00 AM',
#         'attendant': 'Robert',
#     },
#     {
#         'amount': '2300',
#         'time_open': '10:00 AM',
#         'time_close': '4:00 AM',
#         'attendant': 'Joan',
#     },
# ]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
@login_required
def users():
    sales = Sale.query.all()
    return render_template('users.html', sales=sales, title='Kenzen')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(cafe_name=form.cafe_name.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('users'))
        else:
            flash(f'Wrong Information', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
