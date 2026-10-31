"""Traduction français → éwé via NLLB adapté (LoRA).

Le modèle est chargé une seule fois et réutilisé (chargement coûteux en temps
et en mémoire). Aucun poids n'est exposé au frontend ; le modèle est exécuté
exclusivement côté backend.
"""

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


class TranslationUnavailableError(Exception):
    """La traduction n'est pas disponible (modèle absent, non chargé, etc.)."""


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


def _get_translator() -> _Translator:
    global _translator
    with _lock:
        if _translator is None:
            _translator = _Translator()
        return _translator


def translate_fr_to_ewe(text: str) -> str:
    """Traduit un texte français en éwé (appel réel au modèle NLLB)."""
    if not text or not text.strip():
        raise TranslationUnavailableError("Le texte à traduire est vide.")
    try:
        # Sérialise l'inférence : le modèle n'est pas conçu pour des appels concurrents.
        with _infer_lock:
            return _get_translator().translate(text)
    except TranslationUnavailableError:
        raise
    except Exception as exc:
        logger.error("Échec de la traduction : %s", type(exc).__name__)
        raise TranslationUnavailableError("La traduction est momentanément indisponible.") from exc
