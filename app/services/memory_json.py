# app/services/memory_json.py
import json
import os
from datetime import datetime
from typing import Any, Dict
from uuid import uuid4

RUNS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "runs"))

class JsonRunMemory:
    def __init__(self):
        os.makedirs(RUNS_DIR, exist_ok=True)

    def new_run_id(self) -> str:
        return str(uuid4())

    def _path(self, run_id: str) -> str:
        return os.path.join(RUNS_DIR, f"{run_id}.json")

    def init_run(self, run_id: str, rfq: Dict[str, Any]) -> None:
        payload = {
            "run_id": run_id,
            "created_at": datetime.utcnow().isoformat(),
            "rfq": rfq,
            "messages": [],
            "offers": [],
            "negotiation_log": [],
            "escalations": [],
            "result": None,
        }
        self.save(run_id, payload)

    def load(self, run_id: str) -> Dict[str, Any]:
        with open(self._path(run_id), "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, run_id: str, data: Dict[str, Any]) -> None:
        with open(self._path(run_id), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def append_message(self, run_id: str, msg: Dict[str, Any]) -> None:
        data = self.load(run_id)
        data["messages"].append(msg)
        self.save(run_id, data)

    def append_offer(self, run_id: str, offer: Dict[str, Any]) -> None:
        data = self.load(run_id)
        data["offers"].append(offer)
        self.save(run_id, data)

    def set_result(self, run_id: str, result: Dict[str, Any]) -> None:
        data = self.load(run_id)
        data["result"] = result
        self.save(run_id, data)
