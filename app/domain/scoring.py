# app/domain/scoring.py
from typing import Dict, Any
from app.domain.models import RFQ, Offer

def score_offer(rfq: RFQ, offer: Offer) -> Dict[str, Any]:
    score = 0.0

    if offer.total is not None:
        score += max(0.0, 100000.0 / (offer.total + 1.0))

    if offer.lead_time_days is not None:
        score += max(0.0, 50.0 / (offer.lead_time_days + 1.0))

    if offer.payment_terms and offer.payment_terms in rfq.negotiation_policy.payment_terms_preference:
        score += 10.0

    return {
        "supplier": offer.supplier,
        "total": offer.total,
        "lead_time_days": offer.lead_time_days,
        "payment_terms": offer.payment_terms,
        "score": score,
    }
