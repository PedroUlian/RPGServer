* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Poppins", sans-serif;
}

body {
  background-color: #18181b;
  color: #fff;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* ======== Telas ======== */
.screen {
  display: none;
  width: 100%;
  height: 100vh;
}

.screen.active {
  display: flex;
}

/* ======== Tela de login ======== */
#login-screen {
  justify-content: center;
  align-items: center;
  background: #1f1f23;
}

.login-box {
  background: #2b2b2f;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 0 20px rgba(0,0,0,0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  width: 90%;
  max-width: 400px;
}

.login-box h2 {
  margin-bottom: 10px;
}

.login-box input {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 10px;
  background: #3a3a3d;
  color: #fff;
  outline: none;
}

.login-box button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 10px;
  background: #7b5bff;
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s;
}

.login-box button:hover {
  background: #9173ff;
}

/* ======== Chat ======== */
#chat-screen {
  background: #1f1f23;
}

.sidebar {
  width: 250px;
  background: #2b2b2f;
  display: flex;
  flex-direction: column;
  justify-content: start;
  padding: 20px;
  gap: 25px;
  border-radius: 20px 0 0 20px;
}

.sidebar h2 {
  margin-bottom: 10px;
}

.sidebar p {
  cursor: pointer;
  transition: 0.3s;
}

.sidebar p.active {
  color: #a78bfa;
}

.chat-container {
  flex: 1;
  background: #2b2b2f;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
  border-radius: 0 20px 20px 0;
}

#chat-box {
  flex: 1;
  overflow-y: auto;
  background: #444;
  border-radius: 20px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-area {
  display: flex;
  background: #444;
  border-radius: 20px;
  margin-top: 10px;
  padding: 10px;
}

#message-input {
  flex: 1;
  background: none;
  border: none;
  color: #fff;
  outline: none;
  padding: 10px;
  font-size: 1em;
}

#send-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5em;
  cursor: pointer;
  transition: 0.3s;
}

#send-btn:hover {
  transform: scale(1.2);
}

/* ======== Mensagens ======== */
.message {
  background: #5b5b5f;
  padding: 10px 15px;
  border-radius: 15px;
  width: fit-content;
  max-width: 70%;
  word-wrap: break-word;
}

.message.self {
  align-self: flex-end;
  background: #7b5bff;
  color: #fff;
}

/* ======== Responsividade ======== */
@media (max-width: 900px) {
  .sidebar {
    display: none;
  }

  #chat-screen {
    flex-direction: column;
  }

  .chat-container {
    border-radius: 0;
  }

  #chat-box {
    height: 70vh;
  }
}
