# parser.py
import openai
import re

def extract_submit_url(html: str) -> str:
    """
    Extracts the submit URL from the quiz page HTML.
    """
    try:
        # Use OpenAI to extract URL
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract only the submit URL from the HTML."},
                {"role": "user", "content": f"HTML:\n{html}\n\nReturn ONLY the submit URL."}
            ],
            temperature=0
        )
        submit_url = response.choices[0].message.content.strip()
        return submit_url
    except Exception as e:
        print("OpenAI failed, using regex fallback:", e)
        pattern = r"https://[^\s\"']+/submit[^\s\"']*"
        matches = re.findall(pattern, html)
        if matches:
            return matches[0]
        raise ValueError("Submit URL not found")


def extract_question_text(html: str) -> str:
    """
    Extracts the quiz question from the page HTML.
    """
    try:
        # Use OpenAI to extract question
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract only the quiz question from HTML."},
                {"role": "user", "content": f"HTML:\n{html}\n\nReturn ONLY the quiz question."}
            ],
            temperature=0
        )
        question = response.choices[0].message.content.strip()
        return question
    except Exception as e:
        print("OpenAI failed, fallback to raw HTML:", e)
        # fallback: crude extraction
        return html
