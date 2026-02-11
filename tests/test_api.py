"""
API Test Suite
"""

from fastapi.testclient import TestClient
from backend.main import app


class DummyResponse:
    def __init__(self):
        self.content = "Mocked answer"


class DummyDoc:
    def __init__(self):
        self.metadata = {"source": "mock.pdf"}


def dummy_invoke(self, _):
    return DummyResponse()


def dummy_retrieve(self, _):
    return [DummyDoc()]


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


def test_chat_schema():
    with TestClient(app) as client:

        # Inject mock BEFORE request
        app.state.rag_chain = type("MockChain", (), {"invoke": dummy_invoke})()

        app.state.retriever = type("MockRetriever", (), {"invoke": dummy_retrieve})()

        response = client.post(
            "/chat",
            json={"question": "Test question"},
        )

        assert response.status_code == 200

        data = response.json()

        assert "answer" in data
        assert "sources" in data
        assert isinstance(data["sources"], list)
        assert data["answer"] == "Mocked answer"
