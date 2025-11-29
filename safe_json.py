# safe_json.py

from flask import abort

MAX_JSON_MB = 1  # 1 MB limit

def safe_get_json(request):
    """
    Safely parse JSON from a request.
    Returns parsed JSON or raises 400 for invalid JSON.
    """
    # Size check
    try:
        content_length = int(request.headers.get("Content-Length", 0))
    except Exception:
        content_length = 0

    if content_length and content_length > MAX_JSON_MB * 1024 * 1024:
        abort(400, description="Payload too large")

    # JSON parse
    try:
        data = request.get_json(force=True)
    except Exception:
        abort(400, description="Invalid JSON")

    return data
