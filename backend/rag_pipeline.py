"""
RAG Pipeline Module

Initializes the Retrieval-Augmented Generation (RAG) pipeline.
Loads FAISS vector index, connects to Gemini LLM,
and constructs the LangChain Expression Language
 chain for contextual question answering.

Returns:
    - RAG chain
    - Retriever
"""

import os
import logging
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

logging.basicConfig(level=logging.INFO)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "faiss_index")


def get_rag_chain():
    """
    Initializes and returns the RAG chain and retriever.

    Returns:
        tuple: (rag_chain, retriever)
    """

    try:
        logging.info("Initializing embeddings...")

        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

        logging.info("Loading FAISS index...")

        vectorstore = FAISS.load_local(
            INDEX_PATH, embeddings, allow_dangerous_deserialization=True
        )

        retriever = vectorstore.as_retriever(search_kwargs={"k": 7})

        logging.info("Initializing LLM...")

        llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", temperature=0.3)

        prompt = ChatPromptTemplate.from_template("""
You are an AI Interview Assistant.
Use ONLY the provided context to answer.
If the answer is not in context, say "I don't know".

Context:
{context}

Question:
{question}
""")

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()} | prompt | llm
        )

        logging.info("RAG pipeline initialized successfully.")

        return rag_chain, retriever

    except Exception as e:
        logging.error(f"Error initializing RAG pipeline: {e}")
        raise
