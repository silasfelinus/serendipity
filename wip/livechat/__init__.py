from flask import Blueprint
from flask_socketio import SocketIO

livechat_bp = Blueprint('livechat', __name__)
socketio = SocketIO()

from . import routes, events
