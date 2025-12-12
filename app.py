from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from safe_json import safe_get_json
from browser import render_page
from parser import extract_question_text, extract_submit_url
from solver import solve_question
from submitter import submit_answer
from agent import run_task_loop
import os

app = Flask(__name__)
CORS(app)

SECRET = os.environ.get("QUIZ_SECRET")

@app.post("/task")
def task_handler():
    data = safe_get_json(request)
    email = data.get("email")
    secret = data.get("secret")
    url = data.get("url")

    if secret != SECRET:
        abort(403, description="Invalid secret")

    try:
        html, submit_url = render_page(url)   # FIXED
        question = extract_question_text(html)
        answer = solve_question(question)
        submit_response = submit_answer(submit_url, email, secret, answer, url)
    except Exception as e:
        return jsonify({"error": "Failed to load or process quiz page", "details": str(e)}), 500

    return jsonify({
        "status": "ok",
        "question": question,
        "submit_url": submit_url,
        "answer": answer,
        "submit_response": submit_response
    })

@app.post("/run")
def run_agent():
    data = safe_get_json(request)
    start = data.get("start_url")
    email = data.get("email")
    secret = data.get("secret")
    run_task_loop(start, email, secret)
    return {"status": "started"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

