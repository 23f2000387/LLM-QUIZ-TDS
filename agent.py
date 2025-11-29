# agent.py
from browser import render_page
from parser import extract_question_text, extract_submit_url
from solver import solve_question
from submitter import submit_answer

def run_task_loop(start_url: str, email: str, secret: str):
    current_url = start_url

    while current_url:
        print(f"\nFetching task page: {current_url}")

        # 1. Load HTML
        try:
            page_html = render_page(current_url)
        except Exception as e:
            print("Error loading page:", e)
            break

        # 2. Extract question & submit URL
        question = extract_question_text(page_html)
        submit_url = extract_submit_url(page_html)

        print("Question:\n", question)
        print("Submit URL:", submit_url)

        # 3. Solve question
        answer = solve_question(question)
        print("Computed Answer:", answer)

        # 4. Submit Answer
        submit_response = submit_answer(
            submit_url=submit_url,
            email=email,
            secret=secret,
            answer=answer,
            quiz_url=current_url
        )
        print("Submit Response:", submit_response)

        # 5. Get next task URL
        next_url = submit_response.get("url")
        if not next_url:
            print("\nNo next task. Quiz complete!")
            break

        current_url = next_url
