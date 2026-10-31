"""Modèles de requête et de réponse (Pydantic)."""

from pydantic import BaseModel


class ExtractionResponse(BaseModel):
    text: str
    extraction_method: str
    page_count: int | None = None
    warnings: list[str] = []
    request_id: str


class TranslationRequest(BaseModel):
    text: str


class TranslationResponse(BaseModel):
    translation: str
    request_id: str


class ExplanationRequest(BaseModel):
    text: str
    consent: bool = False


class ExplanationItem(BaseModel):
    text: str
    source: str = "ia"


class ExplanationResponse(BaseModel):
    document_nature: str = ""
    objective: str = ""
    summary: str = ""
    obligations: list[ExplanationItem] = []
    rights: list[ExplanationItem] = []
    amounts_payments: list[ExplanationItem] = []
    dates_deadlines: list[ExplanationItem] = []
    conditions_exceptions: list[ExplanationItem] = []
    consequences: list[ExplanationItem] = []
    ambiguities: list[ExplanationItem] = []
    questions: list[ExplanationItem] = []
    request_id: str
