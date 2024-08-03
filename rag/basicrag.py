from dotenv import load_dotenv
import os
from prepare_data import load_data
from typing import List
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.load import dumps, loads
from operator import itemgetter

load_dotenv()


def save_vector_db(
    documents: List[Document],
    embedding: Embeddings,
    path=os.environ["VECTOR_DATABASE_PATH"],
) -> FAISS:
    vector_store = FAISS.from_documents(
        documents=documents, embedding=embedding,
    )
    vector_store.save_local(path)
    return vector_store


def format_docs(docs):
    return "\n\n".join(
        doc.page_content if isinstance(doc, Document) else doc[0].page_content
        for doc in docs
    )


def basic_rag():
    embedding = HuggingFaceEmbeddings(model_name=os.environ["EMBEDDING_MODEL_NAME"])
    vector_store = FAISS.load_local(
        os.environ["VECTOR_DATABASE_PATH"],
        embedding,
        allow_dangerous_deserialization=True,
    )
    retriever = vector_store.as_retriever()
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


if __name__ == "__main__":
    chain = basic_rag()
    chain.invoke("Nguyên tắc sử dụng vũ khí ?")
    