from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/zhblnd/diplom/flask-server/price-tags.db'

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')