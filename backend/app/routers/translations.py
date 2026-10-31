"""Endpoint de traduction français → éwé."""

import uuid

from fastapi import APIRouter, HTTPException

from .. import translation
from ..schemas import TranslationRequest, TranslationResponse

router = APIRouter(prefix="/api/translations", tags=["translations"])

MAX_TEXT_CHARS = 5000


@router.post("", response_model=TranslationResponse)
def create_translation(req: TranslationRequest) -> TranslationResponse:
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Le texte à traduire est vide.")
    if len(text) > MAX_TEXT_CHARS:
        raise HTTPException(status_code=400, detail="Le texte à traduire est trop long.")

    try:
        result = translation.translate_fr_to_ewe(text)
    except translation.TranslationLoadingError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except translation.TranslationUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return TranslationResponse(translation=result, request_id=uuid.uuid4().hex)
