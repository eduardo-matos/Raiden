from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask('raiden')
app.config.from_object('raiden.conf')

db = SQLAlchemy(app)

import views
