"""Modèles de réponse (Pydantic)."""

from pydantic import BaseModel


class ExtractionResponse(BaseModel):
    text: str
    extraction_method: str
    page_count: int | None = None
    warnings: list[str] = []
    request_id: str
