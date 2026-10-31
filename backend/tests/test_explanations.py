import dataclasses
import json

from fastapi.testclient import TestClient

from app.config import settings as real_settings
from app.main import app

client = TestClient(app)


def _post(text, consent):
    return client.post("/api/explanations", json={"text": text, "consent": consent})


def test_requires_consent():
    resp = _post("un texte", False)
    assert resp.status_code == 403


def test_empty_text():
    resp = _post("   ", True)
    assert resp.status_code == 400


def test_no_api_key(monkeypatch):
    no_key = dataclasses.replace(real_settings, gemini_api_key="")
    monkeypatch.setattr("app.ai.settings", no_key)
    resp = _post("un texte", True)
    assert resp.status_code == 503


def test_explain_mocked(monkeypatch):
    class FakeResp:
        output_text = json.dumps(
            {
                "document_nature": "Contrat",
                "objective": "Objet",
                "summary": "Résumé",
                "obligations": [{"text": "Payer", "source": "document"}],
                "rights": [],
                "amounts_payments": [{"text": "100 000 FCFA", "source": "document"}],
                "dates_deadlines": [],
                "conditions_exceptions": [],
                "consequences": [],
                "ambiguities": [{"text": "à vérifier", "source": "incertain"}],
                "questions": [],
            }
        )

    class FakeInteractions:
        def create(self, **kwargs):
            return FakeResp()

    class FakeClient:
        interactions = FakeInteractions()

    monkeypatch.setattr("app.ai._client", lambda: FakeClient())
    resp = _post("un contrat", True)
    assert resp.status_code == 200
    data = resp.json()
    assert data["document_nature"] == "Contrat"
    assert data["obligations"][0]["source"] == "document"
    assert data["ambiguities"][0]["source"] == "incertain"
    assert "request_id" in data


def test_extract_json_fences():
    from app import ai

    assert ai._extract_json('```json\n{"ok": true}\n```') == {"ok": True}
    assert ai._extract_json('{"ok": true}') == {"ok": True}
