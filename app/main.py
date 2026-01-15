# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import router as api_router

app = FastAPI(title=settings.APP_NAME)
app.include_router(api_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME}
