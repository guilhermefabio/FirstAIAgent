# app/domain/policy.py
from app.domain.models import RFQ

def needs_approval(rfq: RFQ, total: float) -> bool:
    return (
        rfq.negotiation_policy.approval_required_over_total > 0
        and total > rfq.negotiation_policy.approval_required_over_total
    )
