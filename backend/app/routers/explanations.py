"""Endpoint d'explication du document via Gemini."""

import uuid

from fastapi import APIRouter, HTTPException

from .. import ai
from ..schemas import ExplanationRequest, ExplanationResponse

router = APIRouter(prefix="/api/explanations", tags=["explanations"])

MAX_TEXT_CHARS = 20000


@router.post("", response_model=ExplanationResponse)
async def create_explanation(req: ExplanationRequest) -> ExplanationResponse:
    # Le consentement est vérifié côté backend, pas seulement dans l'interface.
    if not req.consent:
        raise HTTPException(status_code=403, detail="Consentement requis avant l'analyse.")

    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Le texte à analyser est vide.")
    if len(text) > MAX_TEXT_CHARS:
        raise HTTPException(status_code=400, detail="Le texte à analyser est trop long.")

    try:
        data = ai.explain(text)
    except ai.AIUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return ExplanationResponse(**data, request_id=uuid.uuid4().hex)
