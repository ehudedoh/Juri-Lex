from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_speech_requires_text():
    resp = client.post("/api/speech", json={"text": "   "})
    assert resp.status_code == 400


def test_speech_mocked(monkeypatch):
    monkeypatch.setattr("app.speech.generate_audio", lambda text: b"RIFFfakewavdata")
    monkeypatch.setattr("app.translation.unload", lambda: None)
    resp = client.post("/api/speech", json={"text": "ewe text"})
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "audio/wav"
    assert resp.content == b"RIFFfakewavdata"


def test_speech_unavailable(monkeypatch):
    from app import speech

    def boom(text):
        raise speech.SpeechUnavailableError("modèle indisponible")

    monkeypatch.setattr("app.speech.generate_audio", boom)
    monkeypatch.setattr("app.translation.unload", lambda: None)
    resp = client.post("/api/speech", json={"text": "ewe text"})
    assert resp.status_code == 503
