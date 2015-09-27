from flask.ext.testing import TestCase as FlaskTestCase
from raiden import app, db


dbsession = db.session


def rebuild_schema():
    if 'sqlite' in db.engine.url.drivername:
        db.drop_all()
        db.create_all()
    else:
        raise Exception('Dont dare to test in {}!'.format(db.engine.url.drivername))


class BaseTest(FlaskTestCase):
    def create_app(self):
        app.config.from_object('raiden.conf_test')
        return app

    def __call__(self, *args, **kwargs):
        rebuild_schema()
        return super(BaseTest, self).__call__(*args, **kwargs)
