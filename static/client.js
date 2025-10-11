const socket = io();

const loginScreen = document.getElementById("login-screen");
const chatScreen = document.getElementById("chat-screen");
const loginBtn = document.getElementById("login-btn");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");

const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");

let username = "";

loginBtn.addEventListener("click", () => {
  const name = usernameInput.value.trim();
  const pass = passwordInput.value.trim();

  if (name && pass) {
    username = name;
    localStorage.setItem("username", username);
    loginScreen.classList.remove("active");
    chatScreen.classList.add("active");
  }
});

sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

function sendMessage() {
  const text = messageInput.value.trim();
  if (!text || !username) return;

  const data = { user: username, text };
  socket.send(data);
  messageInput.value = "";
}

socket.on("message", (data) => {
  const msg = document.createElement("div");
  msg.classList.add("message");
  if (data.user === username) msg.classList.add("self");
  msg.innerHTML = `<strong>${data.user}:</strong> ${data.text}`;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
});
