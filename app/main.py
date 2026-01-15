# app/main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.api.routes import router as api_router
from app.api.chat_ui import render_chat_ui

app = FastAPI(title=settings.APP_NAME)
app.include_router(api_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
def chat_ui():
    return render_chat_ui()

@app.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME}
