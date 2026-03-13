from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["adaptive_test_db"]

questions = [
{
"question_text":"Solve: 2x + 4 = 10",
"options":["2","3","4","5"],
"correct_answer":"3",
"difficulty":0.3,
"topic":"Algebra",
"tags":["linear"]
},
{
"question_text":"What is 5 + 7?",
"options":["10","11","12","13"],
"correct_answer":"12",
"difficulty":0.1,
"topic":"Arithmetic",
"tags":["addition"]
}
]

db.questions.insert_many(questions)

print("Questions inserted")
