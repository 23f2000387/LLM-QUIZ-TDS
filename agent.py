import requests
from browser import render_page
from parser import extract_question_text, extract_submit_url
from solver import solve_question
from submitter import submit_answer

def run_task_loop(start_url: str, email: str, secret: str):
    """
    Infinite loop that fetches the next task URL, solves it, and submits the answer
    until the server signals completion.
    """
    current_url = start_url

    while current_url:
        print(f"Fetching task from: {current_url}")

        # 1. Call /task endpoint
        payload = {
            "email": email,
            "secret": secret,
            "url": current_url
        }

        resp = requests.post("http://127.0.0.1:5000/task", json=payload)
        data = resp.json()

        if resp.status_code != 200:
            print("Error:", data)
            break

        # 2. Extract info from response
        question = data.get("question")
        submit_url = data.get("submit_url")
        answer = data.get("answer")

        print("Question:", question)
        print("Answer:", answer)
        print("Submit URL:", submit_url)

        # 3. Submit answer if not already submitted
        submit_response = submit_answer(submit_url, email, secret, answer)
        print("Submit response:", submit_response)

        # 4. Get next task URL (if any)
        next_url = submit_response.get("next_task_url")
        if not next_url:
            print("No more tasks. Quiz complete!")
            break

        current_url = next_url
