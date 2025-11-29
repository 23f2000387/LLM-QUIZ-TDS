# parser.py

import os
import openai
from playwright.sync_api import Page
import re
import os

QUIZ_SECRET = os.environ.get("QUIZ_SECRET")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def extract_submit_url(page: Page) -> str:
    """
    Uses OpenAI to extract the submit URL from the rendered quiz page.
    """
    full_text = page.inner_text("body")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts the submit URL from page text."},
                {"role": "user", "content": f"Here is the full page text:\n\n{full_text}\n\nPlease return only the URL that should be used to submit answers. Return it as plain text."}
            ],
            temperature=0
        )
        submit_url = response.choices[0].message.content.strip()
        return submit_url
    except Exception as e:
        print("OpenAI failed to extract submit URL, falling back to regex:", e)
        # fallback: regex
        import re
        pattern = r"https://[^\s\"']+/submit[^\s\"']*"
        matches = re.findall(pattern, full_text)
        if matches:
            return matches[0]
        raise ValueError("Submit URL not found on page")
    
def extract_question_text(page: Page) -> str:
    """
    Uses OpenAI to extract the actual quiz question from the full page text.
    """
    full_text = page.inner_text("body")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts the quiz question from page text."},
                {"role": "user", "content": f"Here is the full page text:\n\n{full_text}\n\nPlease return only the quiz question in a single concise sentence or paragraph."}
            ],
            temperature=0
        )
        question = response.choices[0].message.content.strip()
        return question
    except Exception as e:
        print("OpenAI failed, returning raw page text:", e)
        return full_text
