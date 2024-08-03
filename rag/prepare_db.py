from dotenv import load_dotenv
import os
from prepare_data import load_data
from typing import List
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


load_dotenv()

def save_vector_db(
    documents: List[Document],
    embedding: Embeddings,
    path=os.environ["VECTOR_DATABASE_PATH"],
) -> FAISS:
    vector_store = FAISS.from_documents(
        documents=documents, embedding=embedding, allow_dangerous_deserialization=True
    )
    vector_store.save_local(path)
    return vector_store


def get_openai_embedding(model_name="text-embedding-3-small"):
    return OpenAIEmbeddings(model=model_name)

def get_huggingface_embedding(model_name=os.environ["EMBEDDING_MODEL_NAME"]):
    return HuggingFaceEmbeddings(model_name)


if __name__ == "__main__":
    docs = load_data("/home/quangster/Workspace/Easy_Law/rag/data/LuatDatDai2013.pkl")
    embedding = get_huggingface_embedding()
    vectorstore = save_vector_db(documents=docs, embedding=embedding)
    print(embedding.embed_query("Vũ khí quân sự"))
