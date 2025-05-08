## Project: RAG Video QA 🎥🤖

### Overview

This project demonstrates how to build a **Retrieval-Augmented Generation (RAG)** system that allows you to ask questions about the content of a long YouTube video.

There are **two ways to interact** with the system:

1. **Notebook-based pipeline** — manually transcribe, embed, and query.
2. **Chatbot interface** — use the Microsoft Bot Framework to chat.

---

### How It Works

Whether using the notebook or chatbot interface, the RAG pipeline follows this process:

- **Transcribe YouTube video** using OpenAI Whisper.
- **Split transcript** into manageable chunks.
- **Embed chunks** using Google Generative AI.
- **Store embeddings** in Pinecone vector database.
- **Answer questions** using Gemini 1.5 Flash via LangChain with semantic search and RAG.


**Note:** We apply a time delay between each request to respect Google GenAI's free tier rate limits. These should be setup in the .env file (see setup section below)

---


### Chatbot Features

- Send a YouTube URL
- Bot transcribes and stores transcript
- Ask follow-up questions about the video
- Uses RAG to find relevant chunks and answer


## Environment Setup

### 1. Install Dependencies

Recommended in a virtual environment:

```bash
pip install -r requirements.txt
```

Add a .env file to the project root:

```ini
PINECONE_API_KEY=your_pinecone_api_key
GOOGLE_API_KEY=your_google_genai_api_key
MAX_REQUESTS_PER_MINUTE=5
REQUEST_INTERVAL=60
```

### 2. Install FFmpeg for Whisper

```bash
# Using Conda
conda install -c conda-forge ffmpeg
```

### 3. Get API Keys

Google Generative AI (Gemini):

* Go to: https://aistudio.google.com/
* Generate an API key and paste it into the .env file.

Pinecone:
* Create an account at https://www.pinecone.io/
* Get your API key from the Pinecone dashboard and paste it into .env.

### 4. Install Bot Framework Emulator

Go to the BotFramework Emulator [Github page](https://github.com/Microsoft/BotFramework-Emulator/releases) and install the latest release for your os.


## Running the Chatbot Locally

Prerequisites:
- Python 3.11+
- Bot Framework Emulator

In the backend directory run:
```bash
uvicorn main:app --reload
```

In the project root directory run:
```bash
python -m bot.app
```

Open in Emulator:

- Enter endpoint URL: http://localhost:3978/api/messages
- Leave App ID and Password blank
- Input a YouTube URL and ask questions about the video!


## Why RAG Instead of Full Transcript?

LLMs have token limits. RAG allows querying long videos by retrieving only relevant content
This makes the solution scalable and efficient


## To Do
- Add support for file uploads
- Handle YouTube transcript fallback if audio fails
- Handle new chat sessions