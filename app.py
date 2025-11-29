# app.py

from flask import Flask, request, jsonify, abort
from safe_json import safe_get_json
from browser import render_page
from parser import extract_submit_url, extract_question_text
from solver import solve_question
from submitter import submit_answer
from agent import run_task_loop
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Optional: enable cross-origin requests

SECRET = os.environ.get("QUIZ_SECRET")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# ---------------------------------------------------------
#  /task  → main endpoint the IITM evaluator calls
# ---------------------------------------------------------
@app.post("/task")
def task_handler():
    data = safe_get_json(request)

    email = data.get("email")
    secret = data.get("secret")
    url = data.get("url")

    if secret != SECRET:
        abort(403, description="Invalid secret")

    try:
        # --- Load quiz page HTML ---
        html = render_page(url)

        # --- Extract question & submit URL ---
        question = extract_question_text(html)
        submit_url = extract_submit_url(html)

        # --- Solve the question ---
        answer = solve_question(question)

        # --- Build submit payload ---
        submit_payload = {
            "email": email,
            "secret": secret,
            "url": url,
            "answer": answer
        }

        # --- Submit the answer ---
        submit_response = submit_answer(submit_url, email, secret, answer, url)

    except Exception as e:
        return jsonify({
            "error": "Failed to load or process quiz page",
            "details": str(e)
        }), 500

    # --- Return everything so agent.py can loop ---
    return jsonify({
        "status": "ok",
        "question": question,
        "submit_url": submit_url,
        "answer": answer,
        "submit_payload": submit_payload,
        "submit_response": submit_response
    }), 200

# ---------------------------------------------------------
#  /run  → local endpoint to test infinite loop
# ---------------------------------------------------------
@app.post("/run")
def run_agent():
    data = safe_get_json(request)
    start = data.get("start_url")
    email = data.get("email")
    secret = data.get("secret")

    run_task_loop(start, email, secret)
    return {"status": "started"}

# ---------------------------------------------------------
# Run Flask App
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
