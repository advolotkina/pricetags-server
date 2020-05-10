from flask import Blueprint
main = Blueprint('main', __name__)
pricetags_app = Blueprint('pricetags_app', __name__)
# если перетащить эти импорты вверх, то всё сломается
from . import views, errors