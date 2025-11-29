# parser.py

import openai
import re

def extract_submit_url(html: str) -> str:
    """
    Extracts submit URL from raw HTML string.
    """
    full_text = html

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract the submit URL from the page text."},
                {"role": "user", "content": f"Page:\n{full_text}\n\nReturn ONLY the submit URL."}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("OpenAI failed, fallback to regex:", e)
        pattern = r"https://[^\s\"']+/submit[^\s\"']*"
        matches = re.findall(pattern, full_text)
        if matches:
            return matches[0]
        raise ValueError("Submit URL not found.")


def extract_question_text(html: str) -> str:
    """
    Extracts quiz question from raw HTML string.
    """
    full_text = html

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract the quiz question from the page text."},
                {"role": "user", "content": f"Page:\n{full_text}\n\nReturn ONLY the quiz question."}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("OpenAI failed, fallback:", e)
        return full_text
