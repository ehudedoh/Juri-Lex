"""Gestion des fichiers temporaires.

Les fichiers importés sont stockés dans `TEMP_DIR/<session_id>/` avec des noms
aléatoires non prédictibles, puis supprimés après traitement. Aucune donnée
n'est conservée durablement.
"""

import os
import secrets
import shutil
import uuid

from .config import settings


def new_session() -> tuple[str, str]:
    """Crée un répertoire de session temporaire et retourne (id, chemin)."""
    os.makedirs(settings.temp_dir, exist_ok=True)
    session_id = uuid.uuid4().hex
    path = os.path.join(settings.temp_dir, session_id)
    os.makedirs(path, exist_ok=True)
    return session_id, path


def save_upload(content: bytes, session_dir: str) -> str:
    """Écrit un fichier importé avec un nom aléatoire non prédictible."""
    dest = os.path.join(session_dir, secrets.token_hex(16))
    with open(dest, "wb") as fh:
        fh.write(content)
    return dest


def cleanup_session(session_dir: str) -> None:
    """Supprime récursivement le répertoire de session."""
    shutil.rmtree(session_dir, ignore_errors=True)
