"""
Prometheus monitoring metrics for AI Interview Assistant.
Tracks requests, latency, errors, and throughput.
"""

from prometheus_client import Counter, Histogram

# Total RAG requests
rag_requests = Counter(
    "rag_requests_total",
    "Total number of RAG chat requests",
)

# RAG errors
rag_errors = Counter(
    "rag_errors_total",
    "Total number of RAG processing errors",
)

# Request latency (in seconds)
rag_latency = Histogram(
    "rag_request_latency_seconds",
    "Latency of RAG responses",
)

# Optional: throughput counter
rag_processed_docs = Counter(
    "rag_processed_documents_total",
    "Total documents retrieved during RAG queries",
)
