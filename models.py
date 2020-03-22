from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/zhblnd/diplom/flask-server/price-tags.db'

# db = SQLAlchemy(app)
from application import db

class PriceTag(db.Model):
    id = db.Column(db.Integer,unique = True, primary_key = True, autoincrement = True)
    serial_number = db.Column(db.String(10), unique = True)
    current_ip = db.Column(db.String(12))
    good_group_id = db.Column(db.Integer)
    last_ping = db.Column(db.DateTime)

    def __init__(self, serial_number, good_group_id):
        self.serial_number = serial_number
        self.good_group_id = good_group_id


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls, serial, curr_ip):
    	pricetag = cls.query.filter_by(serial_number = serial).first()
    	pricetag.current_ip = curr_ip
    	db.session.commit()

class GoodGroup(db.Model):
    id = db.Column(db.Integer,unique = True, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    def __init__(self, name):
        self.name = name

class Good(db.Model):
    id = db.Column(db.Integer,unique = True, primary_key = True, autoincrement = True)
    uid = db.Column(db.String, unique = True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    path_to_pic = db.Column(db.String)
    path_to_specs = db.Column(db.String)

    def __init__(self, uid, name, price):
        self.uid = uid
        self.name = name
        self.price = price

    @classmethod
    def update(cls, curr_uid, new_name, new_price):
        good = cls.query.filter_by(uid = curr_uid).first()
        good.name = new_name
        good.price = new_price
        db.session.commit()

    @classmethod
    def find_pricetag_ip_and_serial(cls, curr_uid):
        good = cls.query.filter_by(uid = curr_uid).first()
        good_id = good.id
        good_to_good_group = GoodToGoodGroup.query.filter_by(good_id = good_id).first()
        group_id = good_to_good_group.good_group_id
        pricetag = PriceTag.query.filter_by(good_group_id = group_id).first()
        return pricetag.current_ip, pricetag.serial_number

class GoodToGoodGroup(db.Model):
    id = db.Column(db.Integer,unique = True, primary_key = True, autoincrement = True)
    good_group_id = db.Column(db.Integer)
    good_id = db.Column(db.Integer)

    def __init__(self, good_group_id, good_id):
        self.good_group_id = good_group_id
        self.good_id = good_id

class Servicer(db.Model):
    id = db.Column(db.Integer,unique = True, primary_key = True, autoincrement = True)
    login = db.Column(db.String, unique = True)
    pass_hash = db.Column(db.String)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Admin(db.Model):
    id = db.Column(db.Integer,unique = True, primary_key = True, autoincrement = True)
    login = db.Column(db.String, unique = True)
    pass_hash = db.Column(db.String)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

# db.create_all()