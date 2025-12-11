import requests

def submit_answer(submit_url: str, email: str, secret: str, answer: str, quiz_url: str) -> dict:
    if not submit_url:
        raise ValueError("submit_url is missing")

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
    except Exception as e:
        return {"error": "Failed to submit answer", "details": str(e)}
