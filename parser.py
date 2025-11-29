# parser.py
from bs4 import BeautifulSoup
import re
import openai

def extract_submit_url(html: str) -> str:
    """
    Extracts submit URL from raw HTML string.
    """
    # Try regex first
    pattern = r"https://[^\s\"']+/submit[^\s\"']*"
    matches = re.findall(pattern, html)
    if matches:
        return matches[0]

    # Fallback to OpenAI
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract the submit URL from the page text."},
                {"role": "user", "content": html}
            ],
            temperature=0
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        raise ValueError("Submit URL not found")

def extract_question_text(html: str) -> str:
    """
    Extracts the quiz question from HTML.
    Handles multiple table rows correctly.
    Returns plain text with rows separated by newlines.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")
        text_rows = []
        for row in rows:
            cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
            text_rows.append(" | ".join(cols))
        return "\n".join(text_rows)

    # fallback: return all visible text
    return soup.get_text(separator="\n", strip=True)
