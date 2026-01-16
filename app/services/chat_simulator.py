# app/services/chat_simulator.py
from typing import Dict, List, Any

from app.core.config import settings
from app.tools.llm.ollama_local import OllamaLLM
from app.tools.llm.openai_api import OpenAILLM
from app.tools.web.price_lookup import fetch_price_signals

class ChatSimulator:
    def __init__(self) -> None:
        self.llm = self._build_llm()

    def _build_llm(self):
        if settings.LLM_PROVIDER.lower() == "openai":
            return OpenAILLM()
        return OllamaLLM()

    def respond(self, message: str, history: List[Dict[str, str]], product: str) -> Dict[str, Any]:
        # Buscar sinais de preço com fallback
        try:
            price_signals = fetch_price_signals(product)
        except Exception as e:
            print(f"[WARN] fetch_price_signals falhou para '{product}': {str(e)}")
            price_signals = []

        system_prompt = self._build_system_prompt(product, price_signals)

        messages = [{"role": "system", "content": system_prompt}]
        for item in history:
            role = "assistant" if item.get("role") == "agent" else "user"
            messages.append({"role": role, "content": item.get("content", "")})
        messages.append({"role": "user", "content": message})

        # Chat com LLM com melhor tratamento de erro
        try:
            reply = self.llm.chat(messages, temperature=0.3)
        except Exception as e:
            error_msg = f"Erro na LLM ({settings.LLM_PROVIDER}): {str(e)}"
            print(f"[ERROR] {error_msg}")
            raise ValueError(error_msg) from e

        return {"reply": reply, "price_signals": price_signals}

    def _build_system_prompt(self, product: str, price_signals: List[Dict[str, str]]) -> str:
        price_lines = []
        for signal in price_signals:
            price = signal.get("price") or "preço não identificado"
            price_lines.append(f"- {signal.get('title')} ({price}) {signal.get('url')}")

        price_block = "\n".join(price_lines) if price_lines else "Sem sinais de preço recentes encontrados."

        return (
            "Você é um agente comprador negociando com um vendedor humano.\n"
            "Contexto: o vendedor não quer usar WhatsApp; a negociação deve acontecer em um chat simulado.\n"
            "Objetivo: convencer o vendedor a fechar uma venda, mantendo o projeto pronto e claro.\n"
            "Produto alvo: "
            f"{product}\n\n"
            "Sinais de preço pesquisados na internet:\n"
            f"{price_block}\n\n"
            "Regras:\n"
            "- Seja educado, direto e profissional.\n"
            "- Faça perguntas objetivas sobre preço, prazo, garantia e disponibilidade.\n"
            "- Use os sinais de preço apenas como referência e deixe isso claro.\n"
            "- Negocie buscando melhor custo-benefício."
        )
