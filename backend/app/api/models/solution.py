from pydantic import BaseModel
from datetime import date
from typing import Optional

class SolutionHintResponse(BaseModel):
    date: date
    hint: str
    
    class Config:
        from_attributes = True

class SolutionCreateRequest(BaseModel):
    date: date
    solution: Optional[str] = None
    hint: Optional[str] = None
    
class SolutionFullResponse(SolutionHintResponse):
    solution: str
    difficulty: int