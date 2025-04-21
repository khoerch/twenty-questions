from datetime import datetime
from typing import Optional
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel


class Solution(BaseModel):
    date: str
    solution: str
    hint: str
    difficulty: int
    created_at: Optional[datetime] = None


def get_db():
    db = firestore.client()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database"""
    cred = credentials.Certificate("./firebase.json")
    firebase_admin.initialize_app(cred)