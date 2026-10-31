"""Endpoint de synthèse vocale éwé (MMS TTS)."""

from fastapi import APIRouter, HTTPException, Response

from .. import speech, translation
from ..schemas import SpeechRequest

router = APIRouter(prefix="/api/speech", tags=["speech"])

MAX_TEXT_CHARS = 2000


@router.post("")
def create_speech(req: SpeechRequest) -> Response:
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Le texte à prononcer est vide.")
    if len(text) > MAX_TEXT_CHARS:
        raise HTTPException(status_code=400, detail="Le texte à prononcer est trop long.")

    # Libère le modèle de traduction (~2,4 Go) avant de charger le TTS (~0,5 Go),
    # afin de rester dans les limites mémoire de la machine (Règle 4).
    translation.unload()

    try:
        wav = speech.generate_audio(text)
    except speech.SpeechUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return Response(
        content=wav,
        media_type="audio/wav",
        headers={
            "Content-Disposition": 'inline; filename="jurilex.wav"',
            "Cache-Control": "no-store",
        },
    )
