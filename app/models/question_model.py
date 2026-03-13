from pydantic import BaseModel
from typing import List


class Question(BaseModel):
    question_text: str
    options: List[str]
    correct_answer: str
    difficulty: float
    topic: str
    tags: List[str]
