// server.js (versão JS equivalente ao testMain)
import express from "express";
import { Server } from "socket.io";
import http from "http";
import pg from "pg";
import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";

dotenv.config();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.json());
app.use(express.static(path.join(__dirname, "public"))); // para servir index.html e front

// 🔹 Conexão PostgreSQL com SSL
const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

// 🔹 Inicializar DB (igualzinho ao que tava antes)
async function initDB() {
  const client = await pool.connect();
  await client.query(`
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS messages (
      id SERIAL PRIMARY KEY,
      user_id INTEGER REFERENCES users(id),
      text TEXT NOT NULL,
      timestamp TIMESTAMPTZ DEFAULT NOW()
    );
  `);
  client.release();
}
initDB().catch(console.error);

// 🔹 Página inicial serve o HTML
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// 🔹 Histórico de mensagens (igual ao Python)
app.get("/history", async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT m.id, u.username, m.text, m.timestamp
      FROM messages m
      JOIN users u ON m.user_id = u.id
      ORDER BY m.id ASC
      LIMIT 100
    `);
    const msgs = result.rows.map(r => ({ user: r.username, text: r.text }));
    res.json(msgs);
  } catch (err) {
    console.error("Erro ao buscar histórico:", err.message);
    res.status(500).json({ error: err.message });
  }
});

// 🔹 Limpar histórico
app.post("/clear_history", async (req, res) => {
  try {
    await pool.query("DELETE FROM messages");
    io.emit("history_cleared");
    res.json({ status: "ok" });
  } catch (err) {
    console.error("Erro ao limpar histórico:", err.message);
    res.status(500).json({ error: err.message });
  }
});

// 🔹 Registro de usuário (igual ao Python)
app.post("/register", async (req, res) => {
  const { username, password } = req.body;
  try {
    const result = await pool.query(
      "INSERT INTO users (username, password) VALUES ($1, $2) RETURNING id",
      [username, password] // ⚠️ Em produção use hash!
    );
    res.json({ status: "ok", user_id: result.rows[0].id });
  } catch (err) {
    console.error("Erro ao registrar usuário:", err.message);
    res.status(400).json({ error: err.message });
  }
});

// 🔹 Login de usuário
app.post("/login", async (req, res) => {
  const { username, password } = req.body;
  try {
    const result = await pool.query(
      "SELECT id FROM users WHERE username=$1 AND password=$2",
      [username, password]
    );
    if (result.rows.length === 0) return res.status(401).json({ error: "Usuário ou senha inválidos" });
    res.json({ status: "ok", user_id: result.rows[0].id });
  } catch (err) {
    console.error("Erro no login:", err.message);
    res.status(500).json({ error: err.message });
  }
});

// 🔹 SocketIO para mensagens em tempo real (igual ao Python)
io.on("connection", (socket) => {
  console.log("Cliente conectado");

  socket.on("message", async (data) => {
    const { user, text } = data;
    if (!user || !text) return;

    try {
      // Buscar user_id pelo username
      const userResult = await pool.query(
        "SELECT id FROM users WHERE username=$1",
        [user]
      );
      if (userResult.rows.length === 0) return;

      const user_id = userResult.rows[0].id;

      await pool.query(
        "INSERT INTO messages (user_id, text) VALUES ($1, $2)",
        [user_id, text]
      );
      io.emit("message", data); // broadcast igual SocketIO do Python
    } catch (err) {
      console.error("Erro ao salvar mensagem:", err.message);
    }
  });

  socket.on("disconnect", () => {
    console.log("Cliente desconectado");
  });
});

// 🔹 Rodar servidor
const PORT = process.env.PORT || 10000;
server.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
