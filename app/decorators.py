from functools import wraps
from flask import abort
from flask_login import current_user
from app.models import Permission