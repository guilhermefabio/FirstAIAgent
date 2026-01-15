# app/api/chat_ui.py
def render_chat_ui() -> str:
    return """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Simulador de Conversa</title>
  <style>
    body {
      font-family: "Inter", system-ui, sans-serif;
      background: #f4f6fb;
      margin: 0;
      padding: 0;
      color: #1f2937;
    }
    .container {
      max-width: 920px;
      margin: 32px auto;
      padding: 24px;
    }
    .header {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-bottom: 16px;
    }
    .header h1 {
      margin: 0;
      font-size: 24px;
    }
    .chat-card {
      background: #ffffff;
      border-radius: 16px;
      box-shadow: 0 12px 30px rgba(15, 23, 42, 0.1);
      padding: 24px;
      display: flex;
      flex-direction: column;
      height: 640px;
    }
    .messages {
      flex: 1;
      overflow-y: auto;
      padding-right: 12px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .message {
      max-width: 70%;
      padding: 12px 16px;
      border-radius: 14px;
      line-height: 1.4;
      font-size: 14px;
    }
    .message.agent {
      background: #e0f2fe;
      align-self: flex-start;
    }
    .message.seller {
      background: #dcfce7;
      align-self: flex-end;
    }
    .meta {
      font-size: 12px;
      color: #6b7280;
      margin-top: 8px;
    }
    .composer {
      display: flex;
      gap: 12px;
      margin-top: 16px;
    }
    .composer textarea {
      flex: 1;
      resize: none;
      border-radius: 12px;
      border: 1px solid #d1d5db;
      padding: 12px;
      font-size: 14px;
    }
    .composer button {
      background: #2563eb;
      color: white;
      border: none;
      border-radius: 12px;
      padding: 12px 20px;
      font-weight: 600;
      cursor: pointer;
    }
    .toolbar {
      display: flex;
      gap: 12px;
      margin-bottom: 12px;
    }
    .toolbar input {
      flex: 1;
      border-radius: 10px;
      border: 1px solid #e5e7eb;
      padding: 8px 12px;
      font-size: 14px;
    }
    .price-box {
      background: #fef3c7;
      border-radius: 12px;
      padding: 12px;
      margin-top: 12px;
      font-size: 13px;
    }
    .price-box ul {
      margin: 8px 0 0;
      padding-left: 18px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Simulador de Conversa (vendedor vs. agente comprador)</h1>
      <p>Você é o vendedor. O agente comprador usa sinais de preço da internet para negociar.</p>
    </div>
    <div class="chat-card">
      <div class="toolbar">
        <input id="productInput" value="Sensor de câmara frigorífica (Termômetro SNMP)" />
      </div>
      <div id="messages" class="messages"></div>
      <div class="composer">
        <textarea id="messageInput" rows="3" placeholder="Digite sua resposta como vendedor..."></textarea>
        <button id="sendBtn">Enviar</button>
      </div>
    </div>
  </div>
  <script>
    const messagesEl = document.getElementById("messages");
    const sendBtn = document.getElementById("sendBtn");
    const messageInput = document.getElementById("messageInput");
    const productInput = document.getElementById("productInput");
    const history = [];

    function renderMessage(role, content, priceSignals = []) {
      const msg = document.createElement("div");
      msg.className = `message ${role}`;
      msg.textContent = content;
      messagesEl.appendChild(msg);

      if (role === "agent" && priceSignals.length) {
        const priceBox = document.createElement("div");
        priceBox.className = "price-box";
        priceBox.innerHTML = `<strong>Sinais de preço usados como referência:</strong>`;
        const list = document.createElement("ul");
        priceSignals.forEach(signal => {
          const item = document.createElement("li");
          item.textContent = `${signal.title} - ${signal.price || "sem preço"} (${signal.url})`;
          list.appendChild(item);
        });
        priceBox.appendChild(list);
        messagesEl.appendChild(priceBox);
      }

      messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    async function sendMessage() {
      const message = messageInput.value.trim();
      if (!message) return;
      renderMessage("seller", message);
      history.push({ role: "seller", content: message });
      messageInput.value = "";

      const response = await fetch("/api/chat/message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          history,
          product: productInput.value.trim()
        })
      });

      const data = await response.json();
      renderMessage("agent", data.reply, data.price_signals || []);
      history.push({ role: "agent", content: data.reply });
    }

    sendBtn.addEventListener("click", sendMessage);
    messageInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
      }
    });

    renderMessage("agent", "Olá! Posso confirmar seu melhor preço para o sensor de câmara frigorífica (Termômetro SNMP)?");
  </script>
</body>
</html>
"""
