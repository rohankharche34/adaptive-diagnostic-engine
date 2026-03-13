from fastapi import APIRouter
from bson import ObjectId

from app.database import sessions_collection, questions_collection
from app.schemas.api_schema import StartSessionRequest, SubmitAnswerRequest
from app.services.adaptive_engine import update_ability
from app.services.question_service import select_next_question
from app.services.ai_insights import generate_study_plan

router = APIRouter()


@router.post("/start-session")
def start_session(data: StartSessionRequest):

    session = {
        "user_id": data.user_id,
        "ability_score": 0.5,
        "questions_answered": [],
        "completed": False
    }

    result = sessions_collection.insert_one(session)

    question = select_next_question(0.5)

    return {
        "session_id": str(result.inserted_id),
        "question": question
    }


@router.post("/submit-answer")
def submit_answer(data: SubmitAnswerRequest):

    session = sessions_collection.find_one({"_id": ObjectId(data.session_id)})

    question = questions_collection.find_one({"_id": ObjectId(data.question_id)})

    correct = data.answer == question["correct_answer"]

    new_ability = update_ability(
        session["ability_score"],
        question["difficulty"],
        correct
    )

    record = {
        "question_id": data.question_id,
        "difficulty": question["difficulty"],
        "correct": correct,
        "topic": question["topic"]
    }

    sessions_collection.update_one(
        {"_id": ObjectId(data.session_id)},
        {
            "$push": {"questions_answered": record},
            "$set": {"ability_score": new_ability}
        }
    )

    session = sessions_collection.find_one({"_id": ObjectId(data.session_id)})

    if len(session["questions_answered"]) >= 10:

        plan = generate_study_plan(
            session["questions_answered"],
            session["ability_score"]
        )

        sessions_collection.update_one(
            {"_id": ObjectId(data.session_id)},
            {"$set": {"completed": True}}
        )

        return {
            "test_completed": True,
            "study_plan": plan
        }

    next_question = select_next_question(new_ability)

    return {
        "correct": correct,
        "new_ability": new_ability,
        "next_question": next_question
    }
