# app/api/schemas.py
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class RunRequest(BaseModel):
    rfq: Dict[str, Any]
    dry_run: bool = True
    channel: str = "whatsapp"

class RunResponse(BaseModel):
    run_id: str
    status: str
    result: Optional[Dict[str, Any]] = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = Field(default_factory=list)
    product: str = "Sensor de câmara frigorífica (Termômetro SNMP)"

class PriceSignal(BaseModel):
    title: str
    url: str
    price: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    price_signals: List[PriceSignal] = Field(default_factory=list)
