import socket
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Good

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/zhblnd/diplom/flask-server/price-tags.db'

# db = SQLAlchemy(app)
from application import db

PORT = 8080

MSG_UPDATE = 0
MSG_RESET = 1
MSG_REBOOT = 2


def update_price_tag(good_uid, name, price):
	# Good.update(good_uid, name, price)
    # host, serial_number = Good.find_pricetag_ip_and_serial(good_uid)
	#достать запись из бд
	#захардкоженный путь
    host = "10.42.0.125"
    # path = "/home/zhblnd/diplom/flask-server/goods/%s" % serial_numbergood_id
    serial_number = "/home/zhblnd/diplom/flask-server/pricetags/test123/good1"
    serial = "test123"
    cmd = "./scp-script.sh %s %s" % (host, serial_number)
    os.system(cmd)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, PORT))
        message = "%s %s" % (serial, MSG_UPDATE)
        print(message)
        s.sendall(bytes(message, "utf8"))
        data = s.recv(1024)
    print('Received', repr(data))


def update_good_name(good_uid):
    pass


def update_good_price(good_uid):
    pass


def update_good_pic(good_uid):
    pass

