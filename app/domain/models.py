# app/domain/models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class BuyerProfile(BaseModel):
    company_name: str
    buyer_name: str
    region: str = "BR"
    language: str = "pt-BR"
    channels_allowed: List[str] = Field(default_factory=lambda: ["whatsapp", "email"])

class Item(BaseModel):
    sku: str
    description: str
    quantity: float
    unit: str
    quality_specs: Optional[str] = None
    max_unit_price: Optional[float] = None

class Demand(BaseModel):
    rfq_id: str
    deadline_quote: Optional[str] = None
    delivery_city: Optional[str] = None
    items: List[Item]
    must_have: List[str] = Field(default_factory=list)
    nice_to_have: List[str] = Field(default_factory=list)

class Supplier(BaseModel):
    name: str
    priority: int = 999
    known_contacts: Dict[str, str] = Field(default_factory=dict)
    constraints: Dict[str, Any] = Field(default_factory=dict)

class NegotiationPolicy(BaseModel):
    target_discount_percent: float = 5.0
    max_discount_percent: float = 12.0
    max_rounds: int = 3
    payment_terms_preference: List[str] = Field(default_factory=lambda: ["14d", "21d"])
    do_not_accept: List[str] = Field(default_factory=list)
    approval_required_over_total: float = 0.0

class RFQ(BaseModel):
    buyer_profile: BuyerProfile
    demand: Demand
    suppliers: List[Supplier] = Field(default_factory=list)
    negotiation_policy: NegotiationPolicy = Field(default_factory=NegotiationPolicy)
    output: Dict[str, Any] = Field(default_factory=dict)

class Offer(BaseModel):
    supplier: str
    items: List[Dict[str, Any]] = Field(default_factory=list)
    total: Optional[float] = None
    freight: Optional[float] = None
    lead_time_days: Optional[int] = None
    payment_terms: Optional[str] = None
    validity: Optional[str] = None
    notes: Optional[str] = None
    raw_text: Optional[str] = None
