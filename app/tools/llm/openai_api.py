# app/tools/llm/openai_api.py
import httpx
from typing import Dict, Any, List
from app.core.config import settings
from app.tools.llm.base import LLMClient

class OpenAILLM(LLMClient):
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is empty")
        self.base_url = settings.OPENAI_BASE_URL.rstrip("/")
        self.model = settings.OPENAI_MODEL

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
        payload = {"model": self.model, "messages": messages, "temperature": temperature}
        r = httpx.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
