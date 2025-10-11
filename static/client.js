const socket = io();
let currentUser = null;

const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");

const chatContainer = document.querySelector(".chat-container");
const loginContainer = document.querySelector(".login-container");
const chatBox = document.getElementById("chat");
const msgInput = document.getElementById("msg");
const sendBtn = document.getElementById("send");
const clearBtn = document.getElementById("clear");

function addMessage(user, text) {
  const p = document.createElement("p");
  p.textContent = `${text}`;
  p.classList.add("message");
  p.classList.add(user === currentUser ? "user" : "other");
  chatBox.appendChild(p);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Login
loginBtn.addEventListener("click", async () => {
  const username = usernameInput.value;
  const password = passwordInput.value;
  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });
  const data = await res.json();
  if (data.status === "ok") {
    currentUser = username;
    loginContainer.style.display = "none";
    chatContainer.style.display = "block";
    loadHistory();
  } else {
    alert(data.error);
  }
});

// Registro
registerBtn.addEventListener("click", async () => {
  const username = usernameInput.value;
  const password = passwordInput.value;
  const res = await fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });
  const data = await res.json();
  if (data.status === "ok") {
    alert("Registrado com sucesso!");
  } else {
    alert(data.error);
  }
});

// Enviar mensagem
sendBtn.addEventListener("click", () => {
  const text = msgInput.value;
  if (!text) return;
  addMessage(currentUser, text);
  socket.emit("message", { user: currentUser, text });
  msgInput.value = "";
});

// Limpar histórico
clearBtn.addEventListener("click", async () => {
  await fetch("/clear_history", { method: "POST" });
  chatBox.innerHTML = "";
});

// Receber mensagens
socket.on("message", data => {
  if (data.user !== currentUser) addMessage(data.user, data.text);
});

// Histórico inicial
async function loadHistory() {
  const res = await fetch("/history");
  const msgs = await res.json();
  chatBox.innerHTML = "";
  msgs.forEach(m => addMessage(m.user, m.text));
}
