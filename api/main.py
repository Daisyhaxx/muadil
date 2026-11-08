"""FastAPI uygulaması: /api altında JSON, kökte web arayüzü.

Çalıştır (proje kökünden): uvicorn api.main:app --reload
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import router

WEB_DIR = Path(__file__).resolve().parents[1] / "web"


class WebFiles(StaticFiles):
    """Tarayıcı her açılışta sunucuya sorar (değişmediyse 304); arayüzün eski hali önbellekte kalmaz."""

    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-cache"
        return response


app = FastAPI(title="Muadil")
app.include_router(router)
app.mount("/", WebFiles(directory=WEB_DIR, html=True), name="web")
