# parser.py
import openai
import re

def extract_submit_url(html: str) -> str:
    """
    Extracts a valid submit URL from HTML, ignoring extra tags.
    """
    # Regex: match HTTPS URL ending with /submit
    matches = re.findall(r"https://[^\s\"'>]+/submit", html)
    if matches:
        return matches[0]  # Return the first valid URL
    raise ValueError("Submit URL not found")

def extract_question_text(html: str) -> str:
    """
    Extracts the quiz question from HTML.
    Tries OpenAI first; falls back to stripping HTML if needed.
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
        # Remove any remaining HTML tags or artifacts
        question = re.sub(r"<[^>]+>", "", question).strip()
        return question

    except Exception as e:
        print("OpenAI failed, fallback to raw HTML extraction:", e)
        # crude fallback: remove all tags
        text = re.sub(r"<[^>]+>", "", html)
        text = re.sub(r"\s+", " ", text)  # normalize whitespace
        return text.strip()
