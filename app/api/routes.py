# app/api/routes.py
from fastapi import APIRouter, HTTPException
from app.api.schemas import RunRequest, RunResponse, ChatRequest, ChatResponse
from app.services.orchestrator import Orchestrator
from app.services.memory_json import JsonRunMemory
from app.services.chat_simulator import ChatSimulator

router = APIRouter()

@router.post("/run", response_model=RunResponse)
def run_agent(payload: RunRequest):
    memory = JsonRunMemory()
    orchestrator = Orchestrator(memory=memory)

    try:
        run_id, result = orchestrator.run(
            rfq=payload.rfq,
            dry_run=payload.dry_run,
            channel=payload.channel,
        )
        return RunResponse(run_id=run_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/chat/message", response_model=ChatResponse)
def chat_message(payload: ChatRequest):
    simulator = ChatSimulator()
    try:
        result = simulator.respond(
            message=payload.message,
            history=[item.model_dump() for item in payload.history],
            product=payload.product,
        )
        return ChatResponse(reply=result["reply"], price_signals=result["price_signals"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
