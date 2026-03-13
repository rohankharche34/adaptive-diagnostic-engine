from pydantic import BaseModel
from typing import List, Optional


class AnswerRecord(BaseModel):
    question_id: str
    difficulty: float
    correct: bool
    topic: str


class UserSession(BaseModel):
    user_id: str
    ability_score: float = 0.5
    questions_answered: List[AnswerRecord] = []
    completed: bool = False
