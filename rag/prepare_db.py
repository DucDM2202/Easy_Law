from dotenv import load_dotenv
import os
from prepare_data import prepare_data, load_docx
from typing import List

from embedding import get_huggingface_embedding
from prepare_data import load_data
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv()

def save_vector_db(
    documents: List[Document],
    embedding: Embeddings,
    path=os.environ["VECTOR_DATABASE_PATH"],
) -> FAISS:
    vector_store = FAISS.from_documents(
        documents=documents, 
        embedding=embedding
    )
    vector_store.save_local(path)
    return vector_store

def prepare_multi_db(embedding: Embeddings):
    """
    Indexing all data from folder ./datapickle to vector database
    """
    folder_path = "./datapickle"

    # Get child folder list
    subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]
    folder_names = [os.path.basename(f) for f in subfolders]

    # Loop
    for i in range(len(folder_names)):
        child_folder_name = folder_names[i]
        subfolder_path = os.path.join(folder_path, child_folder_name)
        files = [f for f in os.listdir(subfolder_path) if f.endswith(".pkl")]
        documents = []
        for file in files:
            file_path = os.path.join(subfolder_path, file)
            docs = load_data(file_path)
            documents.extend(docs)

        # Save to FAISS vector database
        save_vector_db(documents, embedding, f"./faiss/{child_folder_name}")
        print(f"Saved {child_folder_name}, {len(documents)} documents")


if __name__ == "__main__":
    embedding = get_huggingface_embedding()
    documents = load_data("./datapickle/hinh_su/100-2015-QH13.pkl")
    print(documents[0])
    save_vector_db(documents, embedding, path="./faiss/hinh_su")
    # prepare_multi_db(embedding)
