"""
API Test Suite

Contains unit tests for health endpoint and chat response schema.
Ensures API returns correct structure and status codes.
"""

from fastapi.testclient import TestClient
from main import app


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


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_schema():

    # Inject mock BEFORE request
    app.state.rag_chain = type("MockChain", (), {"invoke": dummy_invoke})()

    app.state.retriever = type("MockRetriever", (), {"invoke": dummy_retrieve})()

    response = client.post(
        "/chat",
        json={"question": "Test question"},
    )
    print(response.json())

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)
    assert data["answer"] == "Mocked answer"
