# app/domain/state_machine.py
from enum import Enum

class State(str, Enum):
    INIT = "INIT"
    SUPPLIER_RESOLUTION = "SUPPLIER_RESOLUTION"
    CONTACT_DISCOVERY = "CONTACT_DISCOVERY"
    OUTREACH = "OUTREACH"
    WAIT_REPLY = "WAIT_REPLY"
    PARSE_OFFER = "PARSE_OFFER"
    SCORE = "SCORE"
    NEGOTIATE = "NEGOTIATE"
    CLOSE = "CLOSE"
    REPORT = "REPORT"
