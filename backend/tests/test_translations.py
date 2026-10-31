from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_translation_requires_text():
    resp = client.post("/api/translations", json={"text": "   "})
    assert resp.status_code == 400


def test_translation_mocked(monkeypatch):
    monkeypatch.setattr("app.translation.translate_fr_to_ewe", lambda text: "traduction simulée")
    resp = client.post("/api/translations", json={"text": "bonjour"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["translation"] == "traduction simulée"
    assert "request_id" in data


def test_translation_unavailable(monkeypatch):
    from app import translation

    def boom(text):
        raise translation.TranslationUnavailableError("modèle indisponible")

    monkeypatch.setattr("app.translation.translate_fr_to_ewe", boom)
    resp = client.post("/api/translations", json={"text": "bonjour"})
    assert resp.status_code == 503
