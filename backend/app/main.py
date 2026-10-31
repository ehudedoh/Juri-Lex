"""Point d'entrée FastAPI de JuriLex."""

import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import translation
from .config import settings
from .routers import documents, explanations, speech, translations


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Précharge le modèle de traduction en arrière-plan (non bloquant), pour
    # éviter un chargement de plusieurs minutes pendant une requête HTTP.
    translation.start_loading()
    yield


app = FastAPI(
    title="JuriLex",
    description="Assistance à la compréhension des documents juridiques (Togo).",
    version="0.1.0",
    lifespan=lifespan,
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
app.include_router(speech.router)


@app.get("/api/health")
def health() -> dict:
    """Vérifie l'état général du service (sans exposer d'information interne)."""
    return {
        "status": "ok",
        "translation_model": translation.status(),
        "request_id": uuid.uuid4().hex,
    }
