# app/services/rfq_loader.py
import json
from typing import Dict, Any

def load_rfq_from_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
