# submitter.py
import requests

def submit_answer(submit_url: str, email: str, secret: str, answer: str, quiz_url: str) -> dict:
    """
    Sends the answer to the server and returns JSON response.
    Validates the URL format before submitting.
    """
    if not submit_url or not submit_url.startswith("https://"):
        raise ValueError(f"Invalid submit_url: {submit_url}")

    payload = {
        "email": email,
        "secret": secret,
        "url": quiz_url,
        "answer": answer
    }

    try:
        r = requests.post(submit_url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": "Failed to submit answer",
            "details": str(e)
        }
