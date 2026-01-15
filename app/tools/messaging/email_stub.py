# app/tools/messaging/email_stub.py
from app.tools.messaging.base import Messenger

class EmailStub(Messenger):
    def send(self, to: str, text: str) -> None:
        print(f"[EMAIL_STUB] to={to}\n{text}\n")

    def receive(self, thread_id: str):
        return []
