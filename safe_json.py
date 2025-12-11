from flask import abort

MAX_JSON_MB = 1

def safe_get_json(request):
    try:
        content_length = int(request.headers.get("Content-Length", 0))
    except Exception:
        content_length = 0

    if content_length and content_length > MAX_JSON_MB * 1024 * 1024:
        abort(400, description="Payload too large")

    try:
        data = request.get_json(force=True)
    except Exception:
        abort(400, description="Invalid JSON")

    return data
