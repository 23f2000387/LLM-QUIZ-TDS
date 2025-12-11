from browser import render_page
from parser import extract_question_text, extract_submit_url
from solver import solve_question
from submitter import submit_answer

def run_task_loop(start_url: str, email: str, secret: str):
    current_url = start_url

    while current_url:
        print(f"\nFetching task page: {current_url}")

        try:
            html = render_page(current_url)
        except Exception as e:
            print("Error loading page:", e)
            break

        try:
            question = extract_question_text(html)
            submit_url = extract_submit_url(html)
        except Exception as e:
            print("Error parsing page:", e)
            break

        print("Question:", question)
        print("Submit URL:", submit_url)

        answer = solve_question(question)
        print("Computed Answer:", answer)

        submit_response = submit_answer(submit_url, email, secret, answer, current_url)
        print("Submit Response:", submit_response)

        next_url = submit_response.get("url")
        if not next_url:
            print("Quiz complete!")
            break
        current_url = next_url
