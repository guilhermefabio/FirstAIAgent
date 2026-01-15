# app/tools/llm/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class LLMClient(ABC):
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        raise NotImplementedError
