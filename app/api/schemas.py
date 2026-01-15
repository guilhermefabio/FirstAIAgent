# app/api/schemas.py
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class RunRequest(BaseModel):
    rfq: Dict[str, Any]
    dry_run: bool = True
    channel: str = "whatsapp"

class RunResponse(BaseModel):
    run_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
