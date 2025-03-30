from typing import Optional
from pydantic import BaseModel

class Question(BaseModel):
    text: str

class QuestionEvaluation(BaseModel):
    is_yes_no: bool
    answer: Optional[str] = None
    relevance: Optional[int] = None
    is_correct: Optional[bool] = None 