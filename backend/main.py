from fastapi import FastAPI
from pydantic import BaseModel
from services.transcribe import transcribe_video
from services.embed_and_store import embed_documents
from services.rag_answer import answer_question

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    question: str

@app.post("/process")
def process(req: VideoRequest):
    text = transcribe_video(req.url)
    embed_documents(text)
    return {"status": "ok"}

@app.post("/ask")
def ask(req: QuestionRequest):
    return {"answer": answer_question(req.question)}
