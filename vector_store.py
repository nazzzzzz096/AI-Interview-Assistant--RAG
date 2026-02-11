"""
Vector Store Creation Module

This module loads PDF documents, splits them into text chunks,
generates embeddings using Google Gemini embeddings,
and stores the vectors in a FAISS index.

Part of: AI Interview Assistant (RAG-based system).
"""

import os
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

logging.basicConfig(level=logging.INFO)

DATA_PATH = "data"
INDEX_PATH = "faiss_index"


def load_documents():
    """
    Loads all PDF documents from the data folder.

    Returns:
        list: List of loaded documents.
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data folder '{DATA_PATH}' not found.")

    documents = []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            try:
                loader = PyPDFLoader(os.path.join(DATA_PATH, file))
                docs = loader.load()

                for doc in docs:
                    doc.metadata["source"] = file

                documents.extend(docs)
                logging.info(f"Loaded file: {file}")

            except Exception as e:
                logging.error(f"Error loading {file}: {e}")

    if not documents:
        raise ValueError("No valid PDF documents found.")

    return documents


def create_vector_store():
    """
    Creates FAISS vector store using Gemini embeddings.
    """

    try:
        documents = load_documents()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=200
        )

        docs = text_splitter.split_documents(documents)

        logging.info(f"Total chunks created: {len(docs)}")

        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local(INDEX_PATH)

        logging.info("FAISS index created successfully!")

    except Exception as e:
        logging.error(f"Error creating vector store: {e}")
        raise


if __name__ == "__main__":
    create_vector_store()
