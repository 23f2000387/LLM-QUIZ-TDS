import openai

def solve_question(question_text: str) -> str:
    if not question_text or question_text.strip() == "":
        return ""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You solve IITM quiz tasks. Return only the final numeric or textual answer, no explanations."},
                {"role": "user", "content": question_text}
            ],
            temperature=0
        )

        answer = response.choices[0].message.content.strip()

        # Clean answer (remove quotes, markdown, etc.)
        answer = answer.replace("`", "").replace("\n", " ").strip()

        return answer

    except Exception as e:
        print("❌ OpenAI Failed:", e)
        return "42"   # fallback ONLY when API fails
