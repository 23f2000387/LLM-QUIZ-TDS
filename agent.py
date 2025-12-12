# agent.py
from browser import render_page
from parser import extract_question_text

from solver import solve_question
from submitter import submit_answer

def run_task_loop(start_url: str, email: str, secret: str):
    """
    Infinite loop to fetch each quiz page, extract question,
    solve it, submit answer, and continue to next task.
    """
    current_url = start_url

    while current_url:
        print(f"\nFetching task page: {current_url}")

        # --- 1. Render page and get submit URL ---
        try:
            html, submit_url = render_page(current_url)
            if not submit_url:
                print("Submit URL not found on page.")
                break
        except Exception as e:
            print("Error loading page:", e)
            break

        # --- 2. Extract question ---
        try:
            question = extract_question_text(html)
            if not question:
                print("Question extraction failed")
                break
        except Exception as e:
            print("Error parsing page:", e)
            break

        print("Question:", question)
        print("Submit URL:", submit_url)

        # --- 3. Solve question ---
        answer = solve_question(question)
        print("Computed Answer:", answer)

        # --- 4. Submit answer ---
        submit_response = submit_answer(submit_url, email, secret, answer, current_url)
        print("Submit Response:", submit_response)

        # --- 5. Move to next task ---
        next_url = submit_response.get("url")
        if not next_url:
            print("Quiz complete!")
            break
        current_url = next_url

