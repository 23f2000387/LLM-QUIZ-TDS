def run_task_loop(start_url: str, email: str, secret: str):
    current_url = start_url

    while current_url:
        print(f"\nFetching task page: {current_url}")

        # 1. Load full HTML
        html = render_page(current_url)
        if isinstance(html, dict) and "error" in html:
            print("Error:", html)
            break

        # 2. Extract question and submit URL
        question = extract_question_text(html)
        submit_url = extract_submit_url(html)

        print("Question:", question)
        print("Submit URL:", submit_url)

        # 3. Solve the question using OpenAI
        answer = solve_question(question)
        print("Computed Answer:", answer)

        # 4. Submit the answer
        submit_response = submit_answer(
            submit_url=submit_url,
            email=email,
            secret=secret,
            answer=answer,
            quiz_url=current_url
        )

        print("Submit Response:", submit_response)

        # 5. Next task URL is inside key: "url"
        next_url = submit_response.get("url")

        if not next_url:
            print("Quiz complete!")
            break

        # Move to next page
        current_url = next_url
