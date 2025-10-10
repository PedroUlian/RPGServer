from flask import Flask, jsonify, request
from flask_socketio import SocketIO, send
import psycopg2
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # O Socket.IO já cuida do CORS interno

# 🔹 Conexão com PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pedroulian_postgres_chat_user:g9wUtJlIninJk8dTAvmZGNhNqDAsgDjL@dpg-d3kk083uibrs73fcdm70-a.oregon-postgres.render.com/pedroulian_postgres_chat")

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

# 🔹 Página inicial
@app.route("/")
def home():
    return "Servidor do RPG Chat ativo 🚀"

# 🔹 Histórico de mensagens
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
        print("Erro ao buscar histórico:", e)
        return jsonify({"error": "Erro ao buscar histórico"}), 500

# 🔹 Limpar histórico
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
        print("Erro ao limpar histórico:", e)
        return jsonify({"error": "Erro ao limpar histórico"}), 500

# 🔹 Receber e enviar mensagens em tempo real
@socketio.on("message")
def handle_message(data):
    if not data or "text" not in data or "user" not in data:
        return

    user = data["user"]
    text = data["text"]

    # Salva a mensagem no banco
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
