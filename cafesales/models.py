from datetime import datetime
from cafesales import db, login_manager
from flask_login import UserMixin
import pytz


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    cafe_name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    sales = db.relationship('Sale', backref='owner', lazy=True)
    payable = db.relationship('Payables', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.cafe_name}','{self.email}','{self.image_file}')"


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Singapore')))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Sale('{self.amount}','{self.date_created}')"


class Payables(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payable = db.Column(db.String(60), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.String(60), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Singapore')))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Payables('{self.payable}','{self.amount}','{self.due_date}')"
