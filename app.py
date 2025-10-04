import os
import sqlite3
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "segredo_rpg"

socketio = SocketIO(app, cors_allowed_origins="*")

# ====== BANCO DE DADOS ======
DB_FILE = "chat.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

init_db()

def save_message(user, text):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO messages (user, text) VALUES (?, ?)", (user, text))
        conn.commit()

def get_messages(limit=50):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT user, text, timestamp FROM messages ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        return [{"user": r[0], "text": r[1], "timestamp": r[2]} for r in rows][::-1]

# ============================

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route("/")
def index():
    return "Servidor RPG Chat rodando!"

@app.route("/history")
def history():
    return jsonify(get_messages(50))

@app.route("/clear_history", methods=["POST"])
def clear_history():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM messages")
        conn.commit()
    socketio.emit("history_cleared")
    return jsonify({"status": "ok"})

# SocketIO recebe mensagem
@socketio.on("message")
def handle_message(data):
    user = data.get("user", "Anon")
    text = data.get("text", "")
    if text.strip():
        save_message(user, text)
        print(f"Mensagem de {user}: {text}")
        send({"user": user, "text": text}, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        use_reloader=True,
        log_output=True,
        allow_unsafe_werkzeug=True
    )
