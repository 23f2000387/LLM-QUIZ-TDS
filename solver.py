# solver.py
import os
import openai

QUIZ_SECRET = os.environ.get("QUIZ_SECRET")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def solve_question(question_text: str) -> str:
    """
    Generates the answer for a given quiz question using OpenAI GPT-4.
    Returns only the answer as a string. If OpenAI fails, returns '42'.
    """
    if not question_text or question_text.strip() == "":
        return ""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an IITM quiz solver. Return only the answer, no explanations."},
                {"role": "user", "content": question_text}
            ],
            temperature=0
        )

        # Extract the answer text
        answer = response.choices[0].message.content.strip()

        # Clean answer (remove extra whitespace or Markdown formatting)
        answer = answer.replace("`", "").replace("\n", " ").strip()

        return answer

    except Exception as e:
        print("❌ OpenAI failed:", e)
        # Fallback: always return 42 if API fails
        return "42"
