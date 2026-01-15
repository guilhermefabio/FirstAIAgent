# app/services/orchestrator.py
from datetime import datetime
from typing import Any, Dict, Tuple
from app.domain.models import RFQ, Offer
from app.domain.state_machine import State
from app.domain.scoring import score_offer
from app.tools.llm.ollama_local import OllamaLLM
from app.tools.llm.openai_api import OpenAILLM
from app.core.config import settings
from app.tools.messaging.whatsapp_stub import WhatsAppStub
from app.tools.web.scraper_playwright import extract_contacts_from_url

def _now():
    return datetime.utcnow().isoformat()

class Orchestrator:
    def __init__(self, memory):
        self.memory = memory
        self.llm = self._build_llm()
        self.messenger = WhatsAppStub()

    def _build_llm(self):
        if settings.LLM_PROVIDER.lower() == "openai":
            return OpenAILLM()
        return OllamaLLM()

    def run(self, rfq: Dict[str, Any], dry_run: bool = True, channel: str = "whatsapp") -> Tuple[str, Dict[str, Any]]:
        rfq_obj = RFQ.model_validate(rfq)

        run_id = self.memory.new_run_id()
        self.memory.init_run(run_id, rfq)

        state = State.INIT

        state = State.SUPPLIER_RESOLUTION
        suppliers = rfq_obj.suppliers

        state = State.CONTACT_DISCOVERY
        for s in suppliers:
            if "url" in s.known_contacts and not any(k in s.known_contacts for k in ("whatsapp", "email")):
                contacts = extract_contacts_from_url(s.known_contacts["url"])
                self.memory.append_message(run_id, {
                    "ts": _now(), "direction": "internal", "channel": "web",
                    "supplier": s.name, "text": "contacts_extracted",
                    "meta": contacts,
                })

        state = State.OUTREACH
        for s in suppliers:
            contact = s.known_contacts.get("whatsapp") or s.known_contacts.get("email") or ""
            if not contact:
                self.memory.append_message(run_id, {
                    "ts": _now(), "direction": "internal", "channel": channel,
                    "supplier": s.name, "text": "no_contact_found", "meta": {},
                })
                continue

            msg = self._build_rfq_message(rfq_obj, supplier_name=s.name)
            self.memory.append_message(run_id, {
                "ts": _now(), "direction": "out", "channel": channel,
                "supplier": s.name, "text": msg, "meta": {"to": contact, "dry_run": dry_run},
            })

            if not dry_run:
                self.messenger.send(to=contact, text=msg)

        state = State.WAIT_REPLY

        state = State.PARSE_OFFER
        offers = []

        state = State.SCORE
        score_table = []
        for off in offers:
            score_table.append(score_offer(rfq_obj, off))

        best = None
        if score_table:
            best_supplier = sorted(score_table, key=lambda x: x["score"], reverse=True)[0]["supplier"]
            best = next((o for o in offers if o.supplier == best_supplier), None)

        state = State.REPORT
        result = {
            "run_id": run_id,
            "rfq_id": rfq_obj.demand.rfq_id,
            "state": state.value,
            "offers_count": len(offers),
            "score_table": score_table,
            "best_offer": best.model_dump() if best else None,
        }
        self.memory.set_result(run_id, result)
        return run_id, result

    def _build_rfq_message(self, rfq: RFQ, supplier_name: str) -> str:
        items_lines = []
        for it in rfq.demand.items:
            spec = f" | specs: {it.quality_specs}" if it.quality_specs else ""
            items_lines.append(f"- {it.description} ({it.quantity} {it.unit}){spec}")

        must = f"Obrigatório: {', '.join(rfq.demand.must_have)}" if rfq.demand.must_have else ""
        nice = f"Desejável: {', '.join(rfq.demand.nice_to_have)}" if rfq.demand.nice_to_have else ""
        deadline = f"Prazo para cotação: {rfq.demand.deadline_quote}" if rfq.demand.deadline_quote else ""

        return (
            f"Olá! Aqui é {rfq.buyer_profile.buyer_name} da {rfq.buyer_profile.company_name}.\n"
            f"Preciso de cotação para:\n"
            + "\n".join(items_lines) + "\n\n"
            f"Entrega: {rfq.demand.delivery_city or 'a combinar'}\n"
            f"{deadline}\n"
            f"{must}\n"
            f"{nice}\n\n"
            "Pode me retornar com: preço unitário, prazo, frete, forma de pagamento e validade da proposta?"
        )
