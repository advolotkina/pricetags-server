from flask import Blueprint
main = Blueprint('main', __name__)
pricetags_app = Blueprint('pricetags_app', __name__)
from . import views, errors
