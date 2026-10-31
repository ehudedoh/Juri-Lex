"""Configuration de JuriLex.

Les valeurs sont lues depuis les variables d'environnement (ou un fichier
`.env` en développement). Aucune valeur sensible n'est codée en dur.
"""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-3.5-flash"))
    max_upload_size_mb: int = field(default_factory=lambda: _int("MAX_UPLOAD_SIZE_MB", 20))
    max_document_pages: int = field(default_factory=lambda: _int("MAX_DOCUMENT_PAGES", 20))
    model_cache_dir: str = field(default_factory=lambda: os.getenv("MODEL_CACHE_DIR", ""))
    temp_dir: str = field(default_factory=lambda: os.getenv("TEMP_DIR", "/tmp/jurilex"))
    request_timeout_seconds: int = field(default_factory=lambda: _int("REQUEST_TIMEOUT_SECONDS", 300))
    allowed_origins: str = field(default_factory=lambda: os.getenv("ALLOWED_ORIGINS", "http://localhost:5173"))


settings = Settings()

# Dirige le cache Hugging Face (poids NLLB/MMS TTS) vers MODEL_CACHE_DIR si défini.
# Doit être exécuté avant l'import de `transformers`/`peft` dans les modules.
if settings.model_cache_dir:
    os.environ["HF_HUB_CACHE"] = settings.model_cache_dir
    os.environ["TRANSFORMERS_CACHE"] = settings.model_cache_dir
