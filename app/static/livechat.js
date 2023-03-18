document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const sendButton = document.getElementById('send_button');
    const joinButton = document.getElementById('join_button');
    const leaveButton = document.getElementById('leave_button');
    const messageInput = document.getElementById('message_input');
    const roomInput = document.getElementById('room_input');
    const messagesDiv = document.getElementById('messages');

    // Replace this with your actual username.
    const username = 'YourUsername';

    sendButton.addEventListener('click', () => {
        const message = messageInput.value;
        const room = roomInput.value;

        if (message && room) {
            socket.emit('message', { message, room });
            messageInput.value = '';
        }
    });

    joinButton.addEventListener('click', () => {
        const room = roomInput.value;
        if (room) {
            socket.emit('join', { username, room });
        }
    });

    leaveButton.addEventListener('click', () => {
        const room = roomInput.value;
        if (room) {
            socket.emit('leave', { username, room });
        }
    });

    socket.on('message', (message) => {
        const newMessage = document.createElement('p');
        newMessage.innerText = message;
        messagesDiv.appendChild(newMessage);
    });
});
