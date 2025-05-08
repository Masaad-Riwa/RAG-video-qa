import requests


BACKEND_URL = "http://localhost:8000"

def process_video(url, session_id):
    payload = {"url": url, "session_id": session_id}
    print(f"Sending payload to API: {payload}")
    requests.post(f"{BACKEND_URL}/process", json={"url": url, "session_id": session_id})  

def ask_question(question, session_id):
    res = requests.post(f"{BACKEND_URL}/ask", json={"question": question, "session_id": session_id}) 
    return res.json().get("answer", "I don't know.")
