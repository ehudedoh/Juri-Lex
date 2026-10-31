"""Gestion des fichiers temporaires.

Les fichiers importés sont stockés dans `TEMP_DIR/<session_id>/` avec des noms
aléatoires non prédictibles, puis supprimés après traitement. Aucune donnée
n'est conservée durablement.
"""

import os
import secrets
import shutil
import time
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


def cleanup_orphans(max_age_seconds: int) -> int:
    """Supprime les répertoires de session orphelins plus anciens que la limite.

    Couvre les sessions abandonnées ou interrompues (crash, erreur) dont le
    nettoyage normal n'a pas eu lieu (§6.1 du cahier des charges).
    """
    base = settings.temp_dir
    if not os.path.isdir(base):
        return 0
    now = time.time()
    removed = 0
    for name in os.listdir(base):
        path = os.path.join(base, name)
        if not os.path.isdir(path):
            continue
        try:
            if now - os.path.getmtime(path) > max_age_seconds:
                shutil.rmtree(path, ignore_errors=True)
                removed += 1
        except OSError:
            continue
    return removed
