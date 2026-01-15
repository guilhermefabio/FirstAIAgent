# app/tools/messaging/whatsapp_stub.py
from app.tools.messaging.base import Messenger

class WhatsAppStub(Messenger):
    def send(self, to: str, text: str) -> None:
        print(f"[WHATSAPP_STUB] to={to}\n{text}\n")

    def receive(self, thread_id: str):
        return []
