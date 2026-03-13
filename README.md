AI-DRIVEN ADAPTIVE DIAGNOSTIC ENGINE

OVERVIEW

This project implements a 1-Dimensional Adaptive Testing Prototype designed to dynamically evaluate a student's proficiency level through a sequence of questions whose difficulty adapts based on the student's previous responses.

Traditional assessments present the same questions to every student regardless of ability. This system instead uses an adaptive testing approach where:

- Correct answers lead to harder questions
- Incorrect answers lead to easier questions

By continuously adjusting question difficulty, the system converges on an estimate of the student's ability score more efficiently than fixed tests.

The prototype includes:

- A MongoDB-backed question bank
- A Python FastAPI backend
- An adaptive algorithm based on Item Response Theory (IRT)
- LLM-powered personalized learning insights

The goal of this system is to demonstrate architectural thinking, adaptive algorithm design, and AI-augmented development workflows.


SYSTEM ARCHITECTURE

Client / Postman
        |
        v
   FastAPI Backend
     |      |       |
     v      v       v
 Question  Adaptive  AI Study Plan
 Service   Engine    Generator
     |      |         |
     v      v         v
            MongoDB


COMPONENTS

FastAPI Backend
Responsible for managing user sessions, serving questions, processing answers, and updating ability scores.

MongoDB Database
Stores the question bank, user testing sessions, and answer history.

Adaptive Engine
Implements the Item Response Theory ability update logic.

AI Study Plan Generator
Uses a large language model to generate a personalized study plan based on the student’s weaknesses.


TECH STACK

Backend API: FastAPI
Database: MongoDB
Programming Language: Python
AI Integration: OpenAI API
Data Modeling: Pydantic
Environment Management: python-dotenv


PROJECT STRUCTURE

adaptive-diagnostic-engine/

app/
    main.py
    database.py

    models/
        question_model.py
        session_model.py

    services/
        adaptive_engine.py
        question_service.py
        ai_insights.py

    routes/
        test_routes.py

    schemas/
        api_schema.py

seed_questions.py
requirements.txt
README.md


DESIGN PHILOSOPHY

The project follows separation of concerns:

Routes handle API requests.
Services implement business logic.
Models and schemas handle data validation.
The database layer handles MongoDB connectivity.

This modular structure improves scalability, maintainability, and testability.


PHASE 1 — DATA MODELING (MONGODB)

The system uses two primary collections.


QUESTIONS COLLECTION

Each question includes difficulty metadata used by the adaptive algorithm.

Example document:

{
  "_id": "ObjectId",
  "question_text": "Solve: 2x + 4 = 10",
  "options": ["2", "3", "4", "5"],
  "correct_answer": "3",
  "difficulty": 0.3,
  "topic": "Algebra",
  "tags": ["linear equation"]
}

Fields

question_text   : The actual GRE-style question
options         : Multiple choice options
correct_answer  : Correct answer option
difficulty      : Float between 0.1 and 1.0
topic           : Subject category
tags            : Sub-topic metadata


Difficulty Scale

0.1 – Very easy
0.3 – Easy
0.5 – Medium
0.7 – Hard
0.9 – Very hard


USERSESSION COLLECTION

Tracks the student's progress and ability estimate.

Example document:

{
  "_id": "ObjectId",
  "user_id": "user_123",
  "ability_score": 0.5,
  "questions_answered": [
    {
      "question_id": "...",
      "difficulty": 0.4,
      "correct": true,
      "topic": "Algebra"
    }
  ],
  "completed": false
}

Fields

user_id              : Identifier for the student
ability_score        : Current ability estimate
questions_answered   : History of responses
completed            : Whether the test finished


PHASE 2 — ADAPTIVE ALGORITHM

The adaptive testing logic is inspired by Item Response Theory (IRT).

IRT models the probability that a student answers a question correctly based on:

Student ability (theta)
Question difficulty (b)

Probability formula:

P(correct) = 1 / (1 + e^-(theta - b))


ABILITY UPDATE LOGIC

After each question:

1. Calculate predicted probability of correctness
2. Compare with the actual result
3. Adjust the ability score accordingly

Ability update rule:

new_ability = old_ability + learning_rate * (actual - predicted)

Where:

actual = 1 if correct else 0
predicted = IRT probability
learning_rate ≈ 0.1

This ensures ability evolves gradually instead of jumping randomly.


QUESTION SELECTION STRATEGY

To maximize information gain, the system selects the question whose difficulty is closest to the student’s current ability.

Example:

Student ability: 0.55
Next question difficulty: approximately 0.55

This keeps the test in the student’s optimal challenge zone.


PHASE 3 — AI GENERATED STUDY PLAN

After the test completes (10 questions), the system analyzes:

Topics answered incorrectly
Final ability score
Difficulty levels reached

This data is sent to a language model which generates a personalized 3-step study plan.

Example input:

Weak topics: Algebra, Probability
Final ability: 0.58

Example output:

1. Review algebraic equation manipulation fundamentals
2. Practice GRE probability problem sets
3. Solve mixed medium difficulty timed quizzes

This demonstrates how AI can enhance assessment systems by generating targeted learning recommendations.


API DOCUMENTATION

START TEST SESSION

POST /start-session

Request

{
  "user_id": "student_1"
}

Response

{
  "session_id": "...",
  "question": {...}
}


SUBMIT ANSWER

POST /submit-answer

Request

{
  "session_id": "...",
  "question_id": "...",
  "answer": "B"
}

Response

{
  "correct": true,
  "new_ability": 0.62,
  "next_question": {...}
}


TEST COMPLETION RESPONSE

After 10 questions:

{
  "test_completed": true,
  "study_plan": "..."
}


SETUP INSTRUCTIONS

1. Clone Repository

git clone <repo-url>
cd adaptive-diagnostic-engine


2. Install Dependencies

pip install -r requirements.txt


3. Setup Environment Variables

Create a .env file

MONGO_URI=your_mongodb_connection
OPENAI_API_KEY=your_openai_key


4. Seed Question Database

python seed_questions.py


5. Run Server

uvicorn app.main:app --reload


API documentation will be available at:

http://localhost:8000/docs


AI LOG

AI tools were used throughout development to accelerate implementation and explore design alternatives.

How AI Was Used

ChatGPT and code assistants were used for:

- Generating GRE-style seed questions
- Prototyping the IRT ability update logic
- Assisting with FastAPI boilerplate code
- Reviewing MongoDB schema design
- Suggesting improvements to API structure


Challenges AI Could Not Fully Solve

Some areas required manual design and reasoning:

- Determining an appropriate learning rate for ability updates
- Designing a clean modular architecture
- Ensuring the adaptive algorithm behaved realistically
- Designing the question selection strategy

AI was treated as a productivity assistant rather than a replacement for system design decisions.


EVALUATION GOALS

This prototype focuses on demonstrating:

- System design thinking
- Adaptive algorithm implementation
- API architecture
- AI integration for educational insights

The emphasis is on quality of architecture and logic rather than dataset size.


POSSIBLE FUTURE IMPROVEMENTS

If extended further, the system could support:

- Multi-dimensional IRT models
- Larger question banks
- Difficulty calibration from real user data
- Student analytics dashboards
- Reinforcement-learning question selection
