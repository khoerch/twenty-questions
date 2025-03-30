from pydantic import BaseModel
from datetime import date
from typing import Optional

class SolutionResponse(BaseModel):
    date: date
    hint: str
    
    class Config:
        from_attributes = True

class SolutionCreateRequest(BaseModel):
    date: date
    solution: Optional[str] = None
    hint: Optional[str] = None
    
class SolutionFullResponse(SolutionResponse):
    solution: str
    difficulty: int