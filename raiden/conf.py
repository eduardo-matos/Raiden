import os

DEBUG = os.environ.get('PROD', False)
SECRET_KEY = os.environ.get('SECRET_KEY', 'ops')
SQLALCHEMY_DATABASE_URI = 'sqlite:///'

