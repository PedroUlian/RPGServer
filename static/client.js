const socket = io();

// Login
const loginScreen = document.getElementById('login-screen');
const chatScreen = document.getElementById('chat-screen');
const loginBtn = document.getElementById('login-btn');
const usernameInput = document.getElementById('username');

let username = '';

loginBtn.addEventListener('click', () => {
  const val = usernameInput.value.trim();
  if (!val) return;
  username = val;
  loginScreen.style.display = 'none';
  chatScreen.style.display = 'flex';
});

// Chat
const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');

function addMessage(user, text) {
  const msgDiv = document.createElement('div');
  msgDiv.classList.add('message');
  msgDiv.classList.add(user === username ? 'user' : 'other');
  msgDiv.textContent = text;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight; // scroll automático
}

// Envio de mensagens
sendBtn.addEventListener('click', () => {
  const text = messageInput.value.trim();
  if (!text) return;
  socket.emit('message', { user: username, text });
  messageInput.value = '';
});

messageInput.addEventListener('keypress', e => {
  if(e.key === 'Enter') sendBtn.click();
});

// Receber mensagens
socket.on('message', data => {
  addMessage(data.user, data.text);
});
