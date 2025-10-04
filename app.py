from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "segredo_rpg"
socketio = SocketIO(app, cors_allowed_origins="*")

# Quando um cliente envia mensagem
@socketio.on("message")
def handle_message(msg):
    print("Mensagem recebida:", msg)
    # Repassa para todos conectados
    send(msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, use_reloader=True, log_output=True)
