# -*- coding: utf-8 -*-

import logging
from os import environ
from flask import Flask
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler

app = Flask(__name__)

socketio = SocketIO(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

from app import views

app.logger.info('Startup')