const socket = io();

// Login
const loginScreen = document.getElementById('login-screen');
const chatScreen = document.getElementById('chat-screen');
const loginBtn = document.getElementById('login-btn');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const loginError = document.getElementById('login-error');

let username = '';

// Função de login (simulação, backend real necessário para validar)
loginBtn.addEventListener('click', () => {
  const user = usernameInput.value.trim();
  const pass = passwordInput.value.trim();

  if (!user || !pass) {
    loginError.style.display = 'block';
    loginError.textContent = 'Preencha usuário e senha!';
    return;
  }

  // Aqui você pode validar com backend (POST /login)
  // Para teste, aceitamos qualquer combinação
  username = user;
  loginScreen.style.display = 'none';
  chatScreen.style.display = 'flex';
  loginError.style.display = 'none';
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
