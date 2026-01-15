# app/tools/messaging/base.py
from abc import ABC, abstractmethod

class Messenger(ABC):
    @abstractmethod
    def send(self, to: str, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def receive(self, thread_id: str):
        raise NotImplementedError
