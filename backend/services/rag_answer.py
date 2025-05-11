from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_pinecone import PineconeVectorStore
import os
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
#from dotenv import load_dotenv
from services import dev_settings

#load_dotenv()

def answer_question(question: str, session_id: str) -> str:
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print("Google API Key not found. Please ensure it's set in your .env file.")
        return
    print("Google API Key loaded successfully!")

    retriever = PineconeVectorStore.from_existing_index(
        index_name="youtube-rag",
        embedding=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07"),
        namespace=session_id
    ).as_retriever()

    docs = retriever.get_relevant_documents(question)
    if not docs:
        print("No documents found for the session.")
        return "You need to process a video first before asking questions."


    prompt_template = ChatPromptTemplate.from_template("""
    Answer the question based on the context below. Respond in a full sentence. If you can't answer, say "I don't know."
    
    Context: {context}
    Question: {question}
    """)

    chain = (
        {"context": retriever, "question": lambda x: x}
        | prompt_template
        | ChatGoogleGenerativeAI(
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            model="gemini-1.5-flash"
        )
        | StrOutputParser()
    )

    return chain.invoke(question)
