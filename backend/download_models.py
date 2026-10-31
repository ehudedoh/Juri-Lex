"""Pré-télécharge les modèles (NLLB + LoRA + MMS TTS) dans le cache Hugging Face.

Respecte `MODEL_CACHE_DIR` (défini dans app.config). Utile pour préchauffer le
disque persistant avant le déploiement, afin d'éviter le téléchargement
(~2,5 Go) au premier appel.

Usage (depuis backend/) :
    .venv/bin/python download_models.py
"""

from app.config import settings  # noqa: F401 — définit HF_HUB_CACHE via MODEL_CACHE_DIR
from huggingface_hub import snapshot_download

MODELS = [
    "facebook/nllb-200-distilled-600M",
    "cheriftenga/nllb-200-distilled-600M-ewe-lora-v2",
    "facebook/mms-tts-ewe",
]


def main() -> None:
    for repo in MODELS:
        print(f"Téléchargement de {repo} ...", flush=True)
        snapshot_download(repo_id=repo)
        print(f"  OK : {repo}", flush=True)
    print("Téléchargement terminé.", flush=True)


if __name__ == "__main__":
    main()
