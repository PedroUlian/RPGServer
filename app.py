import os
from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "segredo_rpg"

# SocketIO com CORS liberado
socketio = SocketIO(app, cors_allowed_origins="*")

# Rota raiz para health checks
@app.route("/")
def index():
    return "Servidor RPG Chat rodando!"

# Recebe mensagens do cliente
@socketio.on("message")
def handle_message(data):
    user = data.get("user", "Anon")
    text = data.get("text", "")
    print(f"Mensagem de {user}: {text}")
    # Envia para todos (inclusive quem enviou)
    send({"user": user, "text": text}, broadcast=True)

if __name__ == "__main__":
    # Porta que o Render define via variável de ambiente
    port = int(os.environ.get("PORT", 5000))
    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        use_reloader=True,
        log_output=True,
        allow_unsafe_werkzeug=True
    )
