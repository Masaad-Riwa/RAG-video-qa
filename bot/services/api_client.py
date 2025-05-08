import requests


BACKEND_URL = "http://localhost:8000"

def process_video(url):
    requests.post(f"{BACKEND_URL}/process", json={"url": url})

def ask_question(question):
    res = requests.post(f"{BACKEND_URL}/ask", json={"question": question})
    return res.json().get("answer", "I don't know.")