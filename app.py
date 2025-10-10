from flask import Flask, jsonify, request
from flask_socketio import SocketIO, send
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

#Conexão com PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:senha@dpg-d3kk083uibrs73fcdm70-a.oregon-postgres.render.com:5432/nomedobanco")

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

#Rota de teste
@app.route("/")
def home():
    return "Servidor do RPG Chat ativo 🚀"

# Buscar histórico
@app.route("/history")
def history():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT username, text FROM messages ORDER BY id ASC LIMIT 100;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        msgs = [{"user": r[0], "text": r[1]} for r in rows]
        return jsonify(msgs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Limpar histórico
@app.route("/clear_history", methods=["POST"])
def clear_history():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM messages;")
        conn.commit()
        cur.close()
        conn.close()
        socketio.emit("history_cleared")
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Mensagens Socket.IO
@socketio.on("message")
def handle_message(data):
    if not data or "text" not in data or "user" not in data:
        return

    user = data["user"]
    text = data["text"]

    # Salvar no banco
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (username, text) VALUES (%s, %s);", (user, text))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Erro ao salvar mensagem:", e)

    send(data, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
