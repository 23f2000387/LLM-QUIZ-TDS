import os
import openai
QUIZ_SECRET = os.environ.get("QUIZ_SECRET")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def solve_question(question_text: str) -> str:
    if not question_text:
        return ""

    try:
        # Use OpenAI to generate answer
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful IITM quiz solver."},
                {"role": "user", "content": question_text}
            ],
            temperature=0
        )
        answer = response.choices[0].message.content.strip()
        return answer

    except Exception as e:
        print("LLM failed:", e)

    # Fallback: current heuristics
    return "42"
