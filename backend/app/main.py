"""Point d'entrée FastAPI de JuriLex."""

import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import documents, explanations, translations

app = FastAPI(
    title="JuriLex",
    description="Assistance à la compréhension des documents juridiques (Togo).",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.allowed_origins.split(",") if o.strip()],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(explanations.router)
app.include_router(translations.router)


@app.get("/api/health")
def health() -> dict:
    """Vérifie l'état général du service (sans exposer d'information interne)."""
    return {"status": "ok", "request_id": uuid.uuid4().hex}
