from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_moment import Moment
from flask_user import UserManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
moment = Moment()
bootstrap = Bootstrap()
db = SQLAlchemy()
from .models import User


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    from .main import main as main_blueprint
    from .main import pricetags_app as pricetags_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(pricetags_blueprint, url_prefix='/pricetags/')
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # attach routes and custom error pages here
    return app
