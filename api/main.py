"""FastAPI uygulaması: /api altında JSON, kökte web arayüzü.

Çalıştır (proje kökünden): uvicorn api.main:app --reload
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import router

WEB_DIR = Path(__file__).resolve().parents[1] / "web"

app = FastAPI(title="Muadil")
app.include_router(router)
app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
