from flask import Flask, jsonify, request
from flask_socketio import SocketIO, send
import os
import pg8000.native

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Conexão com PostgreSQL (pg8000)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:senha@dpg-d3kk083uibrs73fcdm70-a.oregon-postgres.render.com:5432/nomedobanco")

def get_conn():
    return pg8000.native.Connection.from_uri(DATABASE_URL)

# Página inicial
@app.route("/")
def home():
    return "Servidor do RPG Chat ativo 🚀"

# Histórico de mensagens
@app.route("/history")
def history():
    try:
        conn = get_conn()
        rows = conn.run("SELECT username, text FROM messages ORDER BY id ASC LIMIT 100;")
        conn.close()
        msgs = [{"user": r[0], "text": r[1]} for r in rows]
        return jsonify(msgs)
    except Exception as e:
        print("Erro ao buscar histórico:", e)
        return jsonify({"error": str(e)}), 500

# Limpar histórico
@app.route("/clear_history", methods=["POST"])
def clear_history():
    try:
        conn = get_conn()
        conn.run("DELETE FROM messages;")
        conn.close()
        socketio.emit("history_cleared")
        return jsonify({"status": "ok"})
    except Exception as e:
        print("Erro ao limpar histórico:", e)
        return jsonify({"error": str(e)}), 500

# Receber e enviar mensagens
@socketio.on("message")
def handle_message(data):
    if not data or "text" not in data or "user" not in data:
        return

    user = data["user"]
    text = data["text"]

    try:
        conn = get_conn()
        conn.run("INSERT INTO messages (username, text) VALUES (:user, :text);", user=user, text=text)
        conn.close()
    except Exception as e:
        print("Erro ao salvar mensagem:", e)

    send(data, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
