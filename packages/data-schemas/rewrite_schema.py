from pydantic import BaseModel
from typing import List


class RewriteSuggestion(BaseModel):
    original: str
    replacement: str


class RewriteResult(BaseModel):
    rewritten_text: str
    suggestions: List[RewriteSuggestion]