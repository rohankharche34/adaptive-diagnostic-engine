import os
from openai import OpenAI
from collections import Counter

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_study_plan(answers, ability):

    wrong_topics = [a["topic"] for a in answers if not a["correct"]]

    topic_counts = Counter(wrong_topics)

    weak_topics = list(topic_counts.keys())

    prompt = f"""
A student completed an adaptive GRE diagnostic test.

Weak topics: {weak_topics}
Final ability score: {ability}

Create a concise 3 step study plan to improve.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
