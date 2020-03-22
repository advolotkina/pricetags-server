import socket
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import PriceTag, GoodGroup, Good, GoodToGoodGroup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/zhblnd/diplom/flask-server/price-tags.db'

db = SQLAlchemy(app)

good_group = GoodGroup(name="goodgroup")
db.session.add(good_group)
db.session.commit()
good = Good(uid = "testuid1", name="Computer", price=32000)
db.session.add(good)
db.session.commit()
good_to_group = GoodToGoodGroup(good_group_id = 0, good_id=0)
db.session.add(good_to_group)
db.session.commit()
pricetag = PriceTag(serial_number = "test123",good_group_id = 0)
db.session.add(pricetag)
db.session.commit()
