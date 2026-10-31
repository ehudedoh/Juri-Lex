import dataclasses
import io

from fastapi.testclient import TestClient

from app.config import settings as real_settings
from app.main import app

client = TestClient(app)

DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def _docx_bytes(paragraphs):
    import docx

    d = docx.Document()
    for p in paragraphs:
        d.add_paragraph(p)
    buf = io.BytesIO()
    d.save(buf)
    return buf.getvalue()


def test_extract_endpoint_docx():
    content = _docx_bytes(["Ceci est un test."])
    resp = client.post(
        "/api/documents/extract",
        files=[("files", ("contrat.docx", content, DOCX_MIME))],
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["extraction_method"] == "docx_text"
    assert "Ceci est un test." in data["text"]
    assert "request_id" in data


def test_extract_endpoint_invalid_type():
    resp = client.post(
        "/api/documents/extract",
        files=[("files", ("fichier.txt", b"juste du texte", "text/plain"))],
    )
    assert resp.status_code == 415


def test_extract_endpoint_empty():
    resp = client.post("/api/documents/extract")
    assert resp.status_code in (400, 422)


def test_extract_endpoint_oversize(monkeypatch):
    small = dataclasses.replace(real_settings, max_upload_size_mb=0)
    monkeypatch.setattr("app.routers.documents.settings", small)
    content = _docx_bytes(["trop gros"])
    resp = client.post(
        "/api/documents/extract",
        files=[("files", ("a.docx", content, DOCX_MIME))],
    )
    assert resp.status_code == 413
