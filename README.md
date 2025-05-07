conda install -c conda-forge ffmpeg



## Project: RAG Video QA

### 🔍 Overview

This project demonstrates how to build a Retrieval-Augmented Generation (RAG) system that allows you to ask questions about the content of a long YouTube video. Instead of feeding the entire video transcript into the language model (which would exceed token limits), this system:
- Transcribes the audio using OpenAI's Whisper.
- Splits the transcript into manageable chunks.
- Embeds the chunks using Google Generative AI embeddings.
- Stores embeddings in Pinecone, a vector database.
- Uses similarity search to retrieve relevant chunks at query time.
- Answers questions using Gemini 1.5 Pro via LangChain.

This approach is more efficient and scalable than providing the entire transcript to a model and enables querying very long videos.

---

### ⚙️ Environment Setup

1. **Install dependencies** (recommended in a virtual environment):

```bash
pip install -r requirements.txt
```

Create a .env file in your project directory with the following content:

```ini
PINECONE_API_KEY=your_pinecone_api_key
GOOGLE_API_KEY=your_google_genai_api_key
```

Replace your_pinecone_api_key and your_google_genai_api_key with actual keys (see next section for help on getting them).

2. **Install ffmpeg for Whisper**
Whisper requires ffmpeg to be installed separately.

If you're using Conda (recommended for Windows):

```bash
conda install -c conda-forge ffmpeg
```

3. **API Keys Setup**
Google Generative AI (Gemini):

Go to: https://aistudio.google.com/

Generate an API key and paste it into the .env file.

Pinecone:

Create an account at https://www.pinecone.io/

Get your API key from the Pinecone dashboard and paste it into .env.

4. **Pinecone Index Setup**
Go to the Pinecone dashboard.

Create and index with custom configuration.

Enter:

Index name: youtube-rag-2 (or match what’s in your script).

Metric: cosine

Dimension: 3072 (matches embedding model output)


Wait for the index to be initialized before proceeding.

### Workflow Summary
Transcribe Video:

Downloads the audio stream from a YouTube video using pytubefix.

Uses whisper to generate a transcript.

Saves transcript to transcription.txt.

Split Transcript:

Uses RecursiveCharacterTextSplitter to split the text into smaller documents suitable for embedding.

Embedding and Storage:

Embeds each chunk using GoogleGenerativeAIEmbeddings.

Stores the embeddings in your Pinecone index.

Applies a 15-second delay between each request to respect Google GenAI's rate limits.

RAG Pipeline (Querying):

Uses similarity search to retrieve only relevant transcript chunks based on a user’s question.

Constructs a prompt using a template.

Feeds this context + question into Gemini Pro to get a grounded, contextual answer.

❓ Why Use RAG Instead of Feeding the Full Transcript?
Language models like Gemini Pro have a token limit. Long videos (like Lex Fridman's interviews) often exceed this limit, making it impractical to pass the full transcript as input.

RAG solves this:

It fetches only relevant parts of the transcript using semantic similarity search.

This keeps prompts small, fast, and within token limits.

It allows you to handle hours of content without compromising on response quality.

### Sample Usage
Once everything is set up, run the script and test with a question like:

```python
chain.invoke("What accelerated the progress of the industry between 1996 and 2007?")
```

You’ll receive a contextual answer grounded in the video transcript.

### Notes
Whisper is used in "base" mode, but you can upgrade to "medium" or "large" for better accuracy.

Ensure that the Pinecone index is correctly configured before embedding begins.

If using large transcripts, consider batching document uploads or increasing delay based on your API limits.