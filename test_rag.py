from backend.rag_pipeline import get_rag_chain

chain, retriever = get_rag_chain()

response = chain.invoke("What is supervised learning?")


print(response.content)
