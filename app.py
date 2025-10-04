import os
import sqlite3
import hashlib
from flask import Flask, jsonify, request, session, send_from_directory
from flask_socketio import SocketIO, send

# ====== CONFIGURAÇÃO DO FLASK ======
app = Flask(__name__)
app.secret_key = "segredo_rpg"
socketio = SocketIO(app, cors_allowed_origins="*")

# ====== BANCO DE DADOS ======
DB_FILE = "chat.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        # mensagens
        c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        # usuários
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """)
        conn.commit()

init_db()

# ====== FUNÇÕES AUXILIARES ======
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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

# ====== ROTAS DE LOGIN/REGISTRO ======
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"status":"error","msg":"Preencha todos os campos"}), 400
    hashed = hash_password(password)
    try:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            conn.commit()
        return jsonify({"status":"ok"})
    except sqlite3.IntegrityError:
        return jsonify({"status":"error","msg":"Usuário já existe"}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    hashed = hash_password(password)
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed))
        user = c.fetchone()
        if user:
            session["user"] = username
            return jsonify({"status":"ok"})
        else:
            return jsonify({"status":"error","msg":"Usuário ou senha incorretos"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"status":"ok"})

# ====== ROTAS DO CHAT ======
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

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
    return jsonify({"status":"ok"})

# ====== SOCKETIO ======
@socketio.on("message")
def handle_message(data):
    user = data.get("user", "Anon")
    text = data.get("text", "")
    if text.strip():
        save_message(user, text)
        print(f"[CHAT] {user}: {text}")
        send({"user": user, "text": text}, broadcast=True)

# ====== EXECUÇÃO ======
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
