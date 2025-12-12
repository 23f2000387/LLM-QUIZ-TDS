# solver.py
import openai
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def solve_question(question_text: str) -> str:
    """
    Generates the answer for a given quiz question using OpenAI GPT-4.
    Prints the question and any errors for debugging.
    """
    question_text = question_text.strip()
    if not question_text:
        print("❌ Empty question received")
        return ""

    print(f"📝 Question: {question_text}")  # Print the question for debugging

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
        answer = answer.replace("`", "").replace("\n", " ").strip()
        print(f"✅ GPT Answer: {answer}")  # Print GPT's answer
        return answer

    except Exception as e:
        print("❌ OpenAI API failed:", e)  # Print the error for debugging
        # Optionally return None or some placeholder
        return None
