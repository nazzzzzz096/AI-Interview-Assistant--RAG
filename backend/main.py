"""
FastAPI Application Entry Point

Provides:
- /health endpoint for monitoring
- /chat endpoint for question answering using RAG
- Rate limiting and exception handling

This service exposes the AI Interview Assistant API.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from rag_pipeline import get_rag_chain
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from slowapi.middleware import SlowAPIMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from monitoring import (
    rag_requests,
    rag_errors,
    rag_latency,
    rag_processed_docs,
)

# ---------------------------
# Lifespan (Startup / Shutdown)
# ---------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rag_chain, app.state.retriever = get_rag_chain()
    yield


app = FastAPI(
    title="AI Interview Assistant RAG API",
    lifespan=lifespan,
)

# ---------------------------
# Prometheus Metrics
# ---------------------------

Instrumentator().instrument(app).expose(app)

# ---------------------------
# Rate Limiter Setup
# ---------------------------

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."},
    )


# ---------------------------
# Request Schema
# ---------------------------


class ChatRequest(BaseModel):
    question: str


# ---------------------------
# Health Check Endpoint
# ---------------------------


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}


# ---------------------------
# Chat Endpoint
# ---------------------------


@app.post("/chat")
@limiter.limit("10/minute")
def chat(request: Request, body: ChatRequest):
    """
    Handles user questions by retrieving relevant documents
    and generating responses using Gemini.
    """

    rag_requests.inc()

    with rag_latency.time():
        try:
            rag_chain = app.state.rag_chain
            retriever = app.state.retriever

            response = rag_chain.invoke(body.question)
            docs = retriever.invoke(body.question)

            rag_processed_docs.inc(len(docs))

            sources = list(set(doc.metadata.get("source", "Unknown") for doc in docs))

            return {
                "answer": response.content,
                "sources": sources,
            }

        except Exception as e:
            rag_errors.inc()

            raise HTTPException(
                status_code=500,
                detail=f"Error processing request: {str(e)}",
            )
