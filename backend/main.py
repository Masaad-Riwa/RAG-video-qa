from fastapi import FastAPI
from pydantic import BaseModel
from services.transcribe import transcribe_video
from services.embed_and_store import embed_documents
from services.rag_answer import answer_question

app = FastAPI()

class VideoRequest(BaseModel):
    url: str
    session_id: str

class QuestionRequest(BaseModel):
    question: str
    session_id: str

@app.post("/process")
def process(req: VideoRequest):
    print(f"Received request: {req}") ##debug
    text = transcribe_video(req.url)
    embed_documents(text, session_id=req.session_id)  # Pass session_id to embedding function
    return {"status": "ok"}

@app.post("/ask")
def ask(req: QuestionRequest):
    print(f"Received request: {req}") ##debug
    return {"answer": answer_question(req.question, session_id=req.session_id)}  # Pass session_id to the answer function
