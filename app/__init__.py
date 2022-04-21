# -*- coding: utf-8 -*-

import logging
from os import environ
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)

socketio = SocketIO(app)

from app import views

app.logger.info('Startup')