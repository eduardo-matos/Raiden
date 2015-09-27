from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO
from flask.ext import assets


app = Flask('raiden')
app.config.from_object('raiden.conf')

socketio = SocketIO(app)
db = SQLAlchemy(app)

# asset config
env = assets.Environment(app)
env.register(
    'js_all',
    assets.Bundle(
        'bower_components/angular/angular.min.js',
        'bower_components/socket.io-client/dist/socket.io.min.js',
        'js/raiden.js',
        'js/raiden.services.js',
        'js/raiden.controllers.js',
        output='js_all.js'
    )
)
env.register(
    'css_all',
    assets.Bundle(
        'bower_components/bootstrap/dist/css/bootstrap.min.css',
        output='css_all.css'
    )
)

# startup views
import views
import api
