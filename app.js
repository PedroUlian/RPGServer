import express from "express";
import { Server } from "socket.io";
import http from "http";
import pg from "pg";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.json());

// 🔹 Conexão com PostgreSQL
const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL
});

// 🔹 Inicializar banco (opcional)
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

// 🔹 Página inicial
app.get("/", (req, res) => {
  res.send("Servidor do RPG Chat ativo 🚀");
});

// 🔹 Registrar usuário
app.post("/register", async (req, res) => {
  const { username, password } = req.body;
  try {
    const result = await pool.query(
      "INSERT INTO users (username, password) VALUES ($1, $2) RETURNING id",
      [username, password] // em produção: hash de senha!
    );
    res.json({ status: "ok", user_id: result.rows[0].id });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// 🔹 Histórico de mensagens
app.get("/history", async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT m.id, u.username, m.text, m.timestamp
      FROM messages m
      JOIN users u ON m.user_id = u.id
      ORDER BY m.timestamp ASC
      LIMIT 100
    `);
    res.json(result.rows);
  } catch (err) {
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
    res.status(500).json({ error: err.message });
  }
});

// 🔹 SocketIO para mensagens em tempo real
io.on("connection", (socket) => {
  console.log("Novo cliente conectado");

  socket.on("message", async (data) => {
    const { user_id, text } = data;
    if (!user_id || !text) return;

    try {
      await pool.query(
        "INSERT INTO messages (user_id, text) VALUES ($1, $2)",
        [user_id, text]
      );
      io.emit("message", data);
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
