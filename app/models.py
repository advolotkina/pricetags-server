from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
import datetime
import os


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Permission:
    ADMIN = 16
    OPERATOR = 3
    SERVICER = 2


class PriceTag(db.Model):
    __tablename__ = 'pricetags'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    serial_number = db.Column(db.String(10), unique=True)
    current_ip = db.Column(db.String(12), default=None)
    last_ping = db.Column(db.DateTime)

    def __init__(self, serial_number):
        self.serial_number = serial_number

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls, serial, curr_ip):
        pricetag = cls.query.filter_by(serial_number=serial).first()
        if pricetag.current_ip is None:
            cmd = "/home/zhblnd/diplom/flask-server/scripts/scp-config.sh %s" % curr_ip
            os.system(cmd)
        pricetag.current_ip = curr_ip
        pricetag.last_ping = datetime.datetime.utcnow()
        db.session.commit()


class Good(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    uid = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    path_to_pic = db.Column(db.String)
    path_to_specs = db.Column(db.String)

    def __init__(self, uid, name, price, pic, specs):
        self.uid = uid
        self.name = name
        self.price = price
        self.path_to_pic = pic
        self.path_to_specs = specs

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class PriceTagToGood(db.Model):
    __tablename__ = 'pricetag_to_goods'
    id = db.Column(db.Integer,  unique=True, primary_key=True, autoincrement=True)
    index = db.Column(db.Integer)
    pricetag_id = db.Column(db.Integer)
    good_id = db.Column(db.Integer)

    def __init__(self, index, pricetag_id, good_id):
        self.index = index
        self.pricetag_id = pricetag_id
        self.good_id = good_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
