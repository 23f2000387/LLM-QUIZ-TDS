from flask import Flask, request, jsonify
import requests
import asyncio
from playwright.async_api import async_playwright

app = Flask(__name__)
SECRET = "your_secret_here"

# --- Fetch JS-rendered page ---
async def fetch_page_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector("body")
        content = await page.content()
        await browser.close()
    return content

# --- Placeholder function to solve quiz ---
def solve_quiz(content):
    return 12345

# --- Submit answer ---
def submit_answer(submit_url, email, secret, url, answer):
    payload = {
        "email": email,
        "secret": secret,
        "url": url,
        "answer": answer
    }
    response = requests.post(submit_url, json=payload)
    return response.json()

# --- API endpoint ---
@app.route("/quiz", methods=["POST"])
def quiz_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    if data.get("secret") != SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    email = data.get("email")
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    content = asyncio.run(fetch_page_content(url))
    answer = solve_quiz(content)
    submit_url = "https://example.com/submit"
    result = submit_answer(submit_url, email, SECRET, url, answer)

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
