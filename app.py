import express from "express";
import http from "http";
import { Server } from "socket.io";
import cors from "cors";
import pkg from "pg";

const { Pool } = pkg;

//Conexão com PostgreSQL
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || "postgresql://usuario:senha@dpg-d3kk083uibrs73fcdm70-a.oregon-postgres.render.com:5432/nomedobanco",
  ssl: { rejectUnauthorized: false },
});

//Teste de conexão
pool.connect()
  .then(() => console.log("✅ Conectado ao PostgreSQL!"))
  .catch(err => console.error("❌ Erro ao conectar ao PostgreSQL:", err));

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: "*" }
});

app.use(cors());
app.use(express.json());

//Buscar histórico
app.get("/history", async (req, res) => {
  try {
    const result = await pool.query("SELECT username AS user, text FROM messages ORDER BY id ASC LIMIT 100");
    res.json(result.rows);
  } catch (err) {
    console.error("Erro ao buscar histórico:", err);
    res.status(500).json({ error: "Erro ao buscar histórico" });
  }
});

//Limpar histórico
app.post("/clear_history", async (req, res) => {
  try {
    await pool.query("DELETE FROM messages");
    io.emit("history_cleared");
    res.json({ status: "ok" });
  } catch (err) {
    console.error("Erro ao limpar histórico:", err);
    res.status(500).json({ error: "Erro ao limpar histórico" });
  }
});

//Conexão Socket.IO
io.on("connection", (socket) => {
  console.log("🟢 Novo usuário conectado:", socket.id);

  socket.on("message", async (data) => {
    if (!data.text || !data.user) return;

    // Salvar no banco
    try {
      await pool.query("INSERT INTO messages (username, text) VALUES ($1, $2)", [data.user, data.text]);
      io.emit("message", data);
    } catch (err) {
      console.error("Erro ao salvar mensagem:", err);
    }
  });

  socket.on("disconnect", () => {
    console.log("🔴 Usuário desconectado:", socket.id);
  });
});

//Rota padrão
app.get("/", (req, res) => {
  res.send("Servidor do RPG Chat ativo 🚀");
});

//Porta(Render usa variável PORT)
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`🌍 Servidor rodando na porta ${PORT}`));
