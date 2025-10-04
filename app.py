import os
from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "segredo_rpg"
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("message")
def handle_message(data):
    user = data.get("user", "Anon")
    text = data.get("text", "")
    print(f"Mensagem de {user}: {text}")
    send({"user": user, "text": text}, broadcast=True)

if __name__ == "__main__":
    # Render define a porta em uma variável de ambiente
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, use_reloader=True, log_output=True, allow_unsafe_werkzeug=True)
