const socket = io.connect('http://' + document.domain + ':' + location.port);

// Define a dynamic chat room identifier (e.g., user IDs)
const senderId = "{{ sender_id }}";  // Replace with actual sender ID
const receiverId = "{{ receiver_id }}";  // Replace with actual receiver ID
const chatRoomId = `${senderId}_${receiverId}`;

// Join the chat room when the page loads
socket.emit('join_chat', { chat_room: chatRoomId });

// Send a message
document.getElementById('send-button').addEventListener('click', function() {
    const message = document.getElementById('message-input').value;
    socket.emit('send_message', { chat_room: chatRoomId, content: message });
});

// Receive and display messages
socket.on('message', function(data) {
    const messageContent = data.content;
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += `<p>${messageContent}</p>`;
});