# parser.py
import openai
import re

def extract_question_text(html: str) -> str:
    """
    Extracts the quiz question from the page HTML.
    Uses OpenAI first; falls back to plain text if it fails.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract only the quiz question from the HTML."},
                {"role": "user", "content": f"HTML:\n{html}\nReturn ONLY the quiz question."}
            ],
            temperature=0
        )
        question = response.choices[0].message.content.strip()
        # Remove any leftover HTML tags
        question = re.sub(r"<[^>]+>", "", question).strip()
        return question

    except Exception as e:
        print("OpenAI failed, falling back to raw text extraction:", e)
        # crude fallback: remove all tags and normalize whitespace
        text = re.sub(r"<[^>]+>", "", html)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
