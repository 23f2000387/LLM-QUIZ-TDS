import requests

def submit_answer(submit_url: str, email: str, secret: str, answer: str, quiz_url: str) -> dict:
    """
    Sends the answer back to the server with email and secret, returns the JSON response.
    Expected response contains next_task_url or a completion signal.
    """

    if not submit_url:
        raise ValueError("submit_url is missing")

    payload = {
        "email": email,
        "secret": secret,
        "url": quiz_url,   # ✅ original quiz URL
        "answer": answer
    }

    try:
        response = requests.post(submit_url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        return {
            "error": "Failed to submit answer",
            "details": str(e)
        }
