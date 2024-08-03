from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from embedding import get_huggingface_embedding


def get_retriever(source: str, embedding: Embeddings):
    return FAISS.load_local(
        f"./faiss/{source}",
        embedding,
        allow_dangerous_deserialization=True,
    ).as_retriever()

def get_vectorstrore(source: str, embedding: Embeddings):
    return FAISS.load_local(
        f"./faiss/{source}",
        embedding,
        allow_dangerous_deserialization=True,
    )

if __name__ == "__main__":
    embedding = get_huggingface_embedding()
    vectorstore = get_vectorstrore("test", embedding)
    relevant_documents = vectorstore.similarity_search_with_relevance_scores(
        "Bộ luật Dân sự Việt Nam quy định về những vấn đề gì ?"
    )
    for doc in relevant_documents:
        print(doc)
        print()
