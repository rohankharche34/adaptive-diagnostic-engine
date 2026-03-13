from pydantic import BaseModel


class StartSessionRequest(BaseModel):
    user_id: str


class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    answer: str
