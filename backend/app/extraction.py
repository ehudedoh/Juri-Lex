"""Extraction de texte depuis les documents importés.

Prend en charge :
- PDF avec texte : extraction directe via `pypdf` ;
- PDF numérisé ou mixte : rendu des pages via `pdftoppm` (Poppler) + OCR ;
- DOCX : extraction des paragraphes et tableaux via `python-docx` ;
- Images : OCR Tesseract (langue française).

Le contenu d'un document est traité comme des données, jamais exécuté.
"""

import glob
import io
import os
import re
import subprocess
import zipfile
from dataclasses import dataclass


class ExtractionError(Exception):
    """Erreur d'extraction dont le message peut être présenté à l'utilisateur."""


@dataclass
class ExtractionResult:
    text: str
    method: str
    page_count: int | None
    warnings: list[str]


# --- Détection du type réel (magic bytes, indépendamment de l'extension) ---

def detect_type(content: bytes) -> str | None:
    if content.startswith(b"%PDF"):
        return "pdf"
    if content[:2] == b"PK":
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as z:
                if "word/document.xml" in z.namelist():
                    return "docx"
        except (zipfile.BadZipFile, OSError):
            pass
    try:
        from PIL import Image

        with Image.open(io.BytesIO(content)) as im:
            im.verify()
            return "image"
    except Exception:
        pass
    return None


# --- PDF ---

def pdf_page_count(path: str) -> int:
    from pypdf import PdfReader

    return len(PdfReader(path).pages)


def _render_pdf_pages(pdf_path: str, session_dir: str, dpi: int = 200) -> list[str]:
    prefix = os.path.join(session_dir, "page")
    proc = subprocess.run(
        ["pdftoppm", "-r", str(dpi), "-png", pdf_path, prefix],
        capture_output=True,
    )
    if proc.returncode != 0:
        raise ExtractionError("Le rendu des pages pour l'OCR a échoué.")

    def page_key(p: str) -> int:
        m = re.search(r"-(\d+)\.png$", p)
        return int(m.group(1)) if m else 0

    return sorted(glob.glob(f"{prefix}-*.png"), key=page_key)


def extract_pdf(path: str, session_dir: str | None = None) -> ExtractionResult:
    from pypdf import PdfReader

    reader = PdfReader(path)
    total = len(reader.pages)
    texts: list[str] = []
    empty: list[int] = []
    for i, page in enumerate(reader.pages):
        try:
            t = (page.extract_text() or "").strip()
        except Exception:
            t = ""
        if not t:
            empty.append(i)
        texts.append(t)

    warnings: list[str] = []
    if empty:
        warnings.append(f"Page(s) sans texte détecté : {[i + 1 for i in empty]}")

    if empty and session_dir:
        images = _render_pdf_pages(pdf_path, session_dir)
        for idx in empty:
            if idx < len(images):
                try:
                    texts[idx] = ocr_image(images[idx])
                except ExtractionError:
                    texts[idx] = ""
        warnings.append(f"OCR appliqué sur {len(empty)} page(s).")

    text = "\n\n".join(t for t in texts if t)
    if empty:
        method = "ocr" if len(empty) == total else "mixed"
    else:
        method = "pdf_text"
    return ExtractionResult(text=text, method=method, page_count=total, warnings=warnings)


# --- DOCX ---

def extract_docx(path: str) -> ExtractionResult:
    try:
        import docx
    except ImportError as exc:
        raise ExtractionError("L'extraction DOCX n'est pas disponible.") from exc

    try:
        document = docx.Document(path)
    except Exception as exc:
        raise ExtractionError("Le fichier DOCX est illisible ou endommagé.") from exc

    parts = [p.text for p in document.paragraphs if p.text.strip()]
    for table in document.tables:
        for row in table.rows:
            parts.append(" | ".join(c.text.strip() for c in row.cells))
    return ExtractionResult(text="\n".join(parts), method="docx_text", page_count=None, warnings=[])


# --- OCR ---

def ocr_image(path: str) -> str:
    try:
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise ExtractionError("L'OCR n'est pas disponible (dépendance manquante).") from exc

    try:
        with Image.open(path) as im:
            return (pytesseract.image_to_string(im, lang="fra") or "").strip()
    except pytesseract.TesseractNotFoundError as exc:
        raise ExtractionError("Le moteur OCR (Tesseract) n'est pas installé.") from exc
    except Exception as exc:
        raise ExtractionError("L'OCR de cette image a échoué.") from exc


def extract_image(path: str) -> ExtractionResult:
    return ExtractionResult(text=ocr_image(path), method="ocr", page_count=1, warnings=[])
