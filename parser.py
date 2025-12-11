# parser.py
import openai
import re

def extract_submit_url(html: str) -> str:
    """
    Extracts a valid submit URL from HTML, ignoring extra tags.
    """
    # Regex to match any https URL ending with /submit
    matches = re.findall(r"https://[^\s\"'>]+/submit", html)
    if matches:
        return matches[0]  # first valid match
    raise ValueError("Submit URL not found")

def extract_question_text(html: str) -> str:
    """
    Extracts the quiz question from HTML.
    Tries OpenAI first, falls back to stripping HTML tags.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract only the quiz question from HTML."},
                {"role": "user", "content": f"HTML:\n{html}\nReturn ONLY the quiz question."}
            ],
            temperature=0
        )
        question = response.choices[0].message.content.strip()
        # Clean any HTML remnants
        question = re.sub(r"<[^>]+>", "", question).strip()
        return question
    except Exception as e:
        print("OpenAI failed, fallback to crude extraction:", e)
        # Fallback: remove all HTML tags
        text = re.sub(r"<[^>]+>", "", html)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
