from app import socketio, app
import os


HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 5000))

# app.logger.info('Starting server on {host}:{port}'.format(host=HOST, port=PORT))
socketio.run(app, host=HOST, port=PORT)