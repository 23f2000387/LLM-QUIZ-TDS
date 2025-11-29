# solver.py
import os
import openai

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def solve_question(question_text: str) -> str:
    """
    Solves the quiz question using OpenAI.
    Returns a plain text answer.
    """
    if not question_text:
        return ""

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful IITM quiz solver. Return ONLY the final answer. No explanations."},
                {"role": "user", "content": question_text}
            ],
            temperature=0
        )
        answer = resp.choices[0].message.content.strip()
        # Clean output
        answer = answer.replace("`", "").replace("\n", " ").strip()
        return answer
    except Exception as e:
        print("❌ OpenAI failed:", e)
        return "42"
