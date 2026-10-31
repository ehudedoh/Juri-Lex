"""Traduction français → éwé via NLLB adapté (LoRA).

Le modèle est chargé **une seule fois** puis réutilisé. Le chargement est coûteux
(plusieurs minutes sur CPU) : il est déclenché **en arrière-plan au démarrage**
via `start_loading()`, afin de ne jamais bloquer une requête HTTP (ce qui
dépasserait le délai d'attente des hébergeurs comme Render et provoquerait un
502). Tant que le modèle n'est pas prêt, la traduction lève
`TranslationLoadingError` (réponse 503 rapide).
"""

import gc
import logging
import threading

logger = logging.getLogger("jurilex.translation")

BASE_MODEL = "facebook/nllb-200-distilled-600M"
ADAPTER = "cheriftenga/nllb-200-distilled-600M-ewe-lora-v2"
SRC_LANG = "fra_Latn"
TGT_LANG = "ewe_Latn"
MAX_TOKENS = 128

_lock = threading.Lock()
_infer_lock = threading.Lock()
_translator = None
_state = "idle"  # idle | loading | loaded | failed
_error = None


class TranslationUnavailableError(Exception):
    """La traduction n'est pas disponible (modèle absent, échec, etc.)."""


class TranslationLoadingError(Exception):
    """Le modèle est en cours de chargement ; réessayer plus tard."""


class _Translator:
    def __init__(self):
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        from peft import PeftModel

        self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        base = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL)
        self.model = PeftModel.from_pretrained(base, ADAPTER)
        self.model.eval()

    def translate(self, text: str) -> str:
        self.tokenizer.src_lang = SRC_LANG
        enc = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=MAX_TOKENS)
        gen = self.model.generate(
            **enc,
            forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(TGT_LANG),
            max_new_tokens=MAX_TOKENS,
            num_beams=4,
        )
        return self.tokenizer.batch_decode(gen, skip_special_tokens=True)[0]


def _load() -> None:
    global _translator, _state, _error
    try:
        translator = _Translator()
        with _lock:
            _translator = translator
            _state = "loaded"
            _error = None
    except Exception as exc:
        logger.error("Échec du chargement du modèle de traduction : %s", type(exc).__name__)
        with _lock:
            _state = "failed"
            _error = type(exc).__name__


def start_loading() -> None:
    """Démarre le chargement du modèle en arrière-plan (non bloquant)."""
    global _state
    with _lock:
        if _state in ("loading", "loaded"):
            return
        _state = "loading"
    threading.Thread(target=_load, daemon=True).start()


def status() -> str:
    """État du modèle : idle, loading, loaded ou failed."""
    return _state


def unload() -> None:
    """Libère le modèle de traduction de la mémoire (chargement coûteux)."""
    global _translator, _state
    with _lock:
        if _translator is not None:
            _translator = None
            _state = "idle"
            gc.collect()


def translate_fr_to_ewe(text: str) -> str:
    """Traduit un texte français en éwé (appel réel au modèle NLLB)."""
    if not text or not text.strip():
        raise TranslationUnavailableError("Le texte à traduire est vide.")

    if _state != "loaded":
        start_loading()
        raise TranslationLoadingError(
            "Le modèle de traduction est en cours de chargement. "
            "Réessayez dans quelques instants."
        )

    try:
        # Sérialise l'inférence : le modèle n'est pas conçu pour des appels concurrents.
        with _infer_lock:
            translator = _translator
            if translator is None:
                raise TranslationLoadingError("Le modèle de traduction est en cours de chargement.")
            return translator.translate(text)
    except (TranslationUnavailableError, TranslationLoadingError):
        raise
    except Exception as exc:
        logger.error("Échec de la traduction : %s", type(exc).__name__)
        raise TranslationUnavailableError("La traduction est momentanément indisponible.") from exc
