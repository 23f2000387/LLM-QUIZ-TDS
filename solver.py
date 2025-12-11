import openai
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def solve_question(question_text: str) -> str:
    if not question_text.strip():
        return ""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an IITM quiz solver. Return only the answer."},
                {"role": "user", "content": question_text}
            ],
            temperature=0
        )
        answer = response.choices[0].message.content.strip()
        return answer.replace("`", "").replace("\n", " ").strip()
    except Exception as e:
        print("OpenAI failed:", e)
        return "42"
