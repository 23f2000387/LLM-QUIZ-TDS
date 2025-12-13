import requests
import time
import os
from bs4 import BeautifulSoup

# ================= CONFIG =================
BASE_URL = "https://tds-llm-analysis.s-anand.net"

EMAIL = "23f2000387@ds.study.iitm.ac.in"
SECRET = "8429175630281947563028194756302819475630"

OPENAI_API_KEY = os.getenv("")
OPENAI_URL = "https://aipipe.org/openai/v1/responses"

HEADERS = {"User-Agent": "AutoQuizAgent/1.0"}

AI_HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}
# =========================================


def fetch_page(url):
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.text


def extract_question(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text("\n", strip=True)


def call_ai(question_text):
    """
    AI must return ONLY the answer.
    """
    payload = {
        "model": "gpt-5-nano",
        "input": (
            "You are solving an online technical quiz.\n"
            "Return ONLY the exact answer required.\n"
            "No explanations.\n"
            "No markdown.\n"
            "If a command is asked, return only the command.\n\n"
            f"{question_text}"
        )
    }

    print("\n🤖 ASKING AI...")

    r = requests.post(OPENAI_URL, headers=AI_HEADERS, json=payload)
    r.raise_for_status()

    result = r.json()

    # AI Pipe response extraction
    answer = result["output"][1]["content"][0]["text"].strip()
    return answer


def submit_answer(full_url, answer):
    payload = {
        "email": EMAIL,
        "secret": SECRET,
        "url": full_url,   # 🔴 FULL URL REQUIRED
        "answer": answer
    }

    r = requests.post(f"{BASE_URL}/submit", json=payload)
    r.raise_for_status()
    return r.json()


def main():
    current_url = f"{BASE_URL}/project2"

    while True:
        print("\n==============================")
        print("🌐 FETCHING:", current_url)

        html = fetch_page(current_url)
        question = extract_question(html)

        print("\n📝 QUESTION:\n")
        print(question[:2000])

        answer = call_ai(question)

        print("\n✅ ANSWER:")
        print(answer)

        response = submit_answer(current_url, answer)

        print("\n📝 SUBMISSION RESPONSE:")
        print(response)

        if response.get("delay"):
            time.sleep(response["delay"])

        next_url = response.get("url")
        if not next_url:
            print("\n🏁 QUIZ FINISHED")
            break

        current_url = next_url


if __name__ == "__main__":
    main()
