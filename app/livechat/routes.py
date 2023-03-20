from flask import render_template
from flask_socketio import join_room, leave_room, emit
from app import socketio
from . import livechat_bp

@livechat_bp.route('/')
def livechat():
    return render_template('livechat.html')

@socketio.on("join_room")
def handle_join_room_event(data):
    join_room(data["room"])
    emit("announce", f"{data['username']} has joined the room", room=data["room"])

@socketio.on("leave_room")
def handle_leave_room_event(data):
    leave_room(data["room"])
    emit("announce", f"{data['username']} has left the room", room=data["room"])

@socketio.on("send_message")
def handle_send_message_event(data):
    emit("receive_message", data, room=data["room"])