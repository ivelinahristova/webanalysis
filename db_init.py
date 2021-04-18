import os

import sqlalchemy

from app import app
from app.models import *

with app.app_context():
    db.init_app(app)

    schema = os.environ.get('DATABASE_NAME')
    engine = sqlalchemy.create_engine(os.environ.get('DATABASE_URL'))
    engine.execute(f'CREATE SCHEMA IF NOT EXISTS `{schema}`;')
    engine.execute(f'USE {schema};')

    db.create_all()
