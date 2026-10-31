"""Synthèse vocale éwé via MMS TTS (VITS).

Le modèle est chargé à la demande (une seule fois) puis peut être libéré.
Aucun poids n'est exposé au frontend ; la génération s'exécute côté backend.
"""

import gc
import io
import logging
import threading
import wave

import numpy as np

logger = logging.getLogger("jurilex.speech")

MODEL = "facebook/mms-tts-ewe"

_lock = threading.Lock()
_tts = None


class SpeechUnavailableError(Exception):
    """La synthèse vocale n'est pas disponible."""


class _TTS:
    def __init__(self):
        from transformers import VitsModel, AutoTokenizer

        self.model = VitsModel.from_pretrained(MODEL)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        self.sample_rate = int(self.model.config.sampling_rate)

    def generate(self, text: str):
        import torch

        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            waveform = self.model(**inputs).waveform
        return waveform.squeeze().numpy()


def _to_wav_bytes(waveform, sample_rate: int) -> bytes:
    audio = np.clip(waveform, -1.0, 1.0)
    pcm = (audio * 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16 bits
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.tobytes())
    return buf.getvalue()


def unload() -> None:
    """Libère le modèle TTS de la mémoire."""
    global _tts
    with _lock:
        _tts = None
        gc.collect()


def generate_audio(text: str) -> bytes:
    """Génère un fichier WAV (octets) à partir d'un texte éwé."""
    if not text or not text.strip():
        raise SpeechUnavailableError("Le texte à prononcer est vide.")

    global _tts
    try:
        with _lock:
            if _tts is None:
                _tts = _TTS()
            waveform = _tts.generate(text)
            sample_rate = _tts.sample_rate
        return _to_wav_bytes(waveform, sample_rate)
    except SpeechUnavailableError:
        raise
    except Exception as exc:
        logger.error("Échec de la synthèse vocale : %s", type(exc).__name__)
        raise SpeechUnavailableError("La génération audio a échoué.") from exc
