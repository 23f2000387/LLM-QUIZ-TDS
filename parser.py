import openai
import re

def extract_submit_url(html: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract only the submit URL from HTML."},
                {"role": "user", "content": f"HTML:\n{html}\nReturn ONLY the submit URL."}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI failed, using regex fallback:", e)
        matches = re.findall(r"https://[^\s\"']+/submit[^\s\"']*", html)
        if matches:
            return matches[0]
        raise ValueError("Submit URL not found")

def extract_question_text(html: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract only the quiz question from HTML."},
                {"role": "user", "content": html}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI failed, fallback to raw HTML:", e)
        return html
