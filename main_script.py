import os
import datetime
from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Role, PriceTag
from flask_moment import Moment

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, PriceTag=PriceTag, datetime=datetime, moment=Moment)

