from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Configurable rate limits
MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE"))
REQUEST_INTERVAL = int(os.getenv("REQUEST_INTERVAL"))  # seconds
DELAY_BETWEEN_DOCS = REQUEST_INTERVAL / MAX_REQUESTS_PER_MINUTE  # e.g., 12s


def embed_documents(text: str, session_id: str):
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print("Google API Key not found. Please ensure it's set in your .env file.")
        return
    print("Google API Key loaded successfully!")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=20)
    docs = splitter.split_documents([Document(page_content=text)])

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07")
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index("youtube-rag")

    vectorstore = PineconeVectorStore.from_existing_index(index_name="youtube-rag", embedding=embeddings, namespace=session_id)

    for idx, doc in enumerate(docs):
        print(f"Embedding document {idx + 1} of {len(docs)}...")

        try:
            vectorstore.add_documents([doc])
            print(f"Processed document {idx + 1}/{len(docs)}.")
        except Exception as e:
            print(f"Error processing document {idx + 1}: {e}")

        # Wait before next request if not the last doc
        if idx < len(docs) - 1:
            print(f"Waiting {DELAY_BETWEEN_DOCS} seconds to avoid rate limit...")
            time.sleep(DELAY_BETWEEN_DOCS)
