"""Endpoint d'extraction de texte depuis un document importé."""

import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile

from .. import extraction, storage
from ..config import settings
from ..schemas import ExtractionResponse

router = APIRouter(prefix="/api/documents", tags=["documents"])


async def _read_upload(file: UploadFile, max_bytes: int) -> bytes:
    data = bytearray()
    while chunk := await file.read(1024 * 1024):
        data.extend(chunk)
        if len(data) > max_bytes:
            raise HTTPException(status_code=413, detail="Le fichier est trop volumineux.")
    if not data:
        raise HTTPException(status_code=400, detail="Fichier vide.")
    return bytes(data)


@router.post("/extract", response_model=ExtractionResponse)
async def extract_document(files: list[UploadFile] = File(...)) -> ExtractionResponse:
    if not files:
        raise HTTPException(status_code=400, detail="Aucun fichier reçu.")
    if len(files) > settings.max_document_pages:
        raise HTTPException(status_code=400, detail="Trop de pages importées.")

    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    _, session_dir = storage.new_session()

    results: list[extraction.ExtractionResult] = []
    total_pages = 0
    try:
        for file in files:
            content = await _read_upload(file, max_bytes)
            ftype = extraction.detect_type(content)
            if ftype is None:
                raise HTTPException(status_code=415, detail="Format de fichier non pris en charge.")
            path = storage.save_upload(content, session_dir)

            if ftype == "pdf":
                pages = extraction.pdf_page_count(path)
                total_pages += pages
                if pages > settings.max_document_pages:
                    raise HTTPException(status_code=400, detail="Le document contient trop de pages.")
                results.append(extraction.extract_pdf(path, session_dir))
            elif ftype == "docx":
                total_pages += 1
                results.append(extraction.extract_docx(path))
            else:  # image
                total_pages += 1
                results.append(extraction.extract_image(path))

        if total_pages > settings.max_document_pages:
            raise HTTPException(status_code=400, detail="Le document contient trop de pages.")
    except HTTPException:
        raise
    except extraction.ExtractionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="L'extraction a échoué. Vérifiez le document.") from exc
    finally:
        storage.cleanup_session(session_dir)

    text = "\n\n".join(r.text for r in results if r.text)
    methods = {r.method for r in results}
    method = methods.pop() if len(methods) == 1 else "mixed"
    page_count = sum(r.page_count for r in results if r.page_count is not None) or None
    warnings = [w for r in results for w in r.warnings]

    return ExtractionResponse(
        text=text,
        extraction_method=method,
        page_count=page_count,
        warnings=warnings,
        request_id=uuid.uuid4().hex,
    )
