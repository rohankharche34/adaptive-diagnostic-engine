from app.database import questions_collection


def get_question_by_id(qid):
    return questions_collection.find_one({"_id": qid})


def get_all_questions():

    return list(questions_collection.find())


def select_next_question(ability):

    questions = list(questions_collection.find())

    questions.sort(key=lambda q: abs(q["difficulty"] - ability))

    return questions[0]
