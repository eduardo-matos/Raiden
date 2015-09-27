from datetime import datetime
from . import db


class Task(db.Model):
    __table_name__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    item_count = db.Column(db.Integer, nullable=False)
    slug = db.Column(db.String(32), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
