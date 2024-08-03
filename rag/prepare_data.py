from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents import Document
import pickle
from typing import List
import os


def load_docx(file_path) -> List[Document]:
    loader = Docx2txtLoader(file_path)
    documents = loader.load()
    return documents


def split_law_text(text: str) -> List[str]:
    chuongs = text.split("\n\nChương")
    chuongs = chuongs[1:]
    results = []
    for chuong in chuongs:
        chuong = chuong.strip()
        if "\n\nMục" in chuong:
            mucs = chuong.split("\n\nMục")
            ten_chuong = mucs[0].strip().replace("\n", " ").replace("  ", " ")
            mucs = mucs[1:]
            for muc in mucs:
                muc = muc.strip()
                dieus = muc.split("\n\nĐiều")
                ten_muc = dieus[0].strip().replace("\n", " ").replace("  ", " ")
                dieus = dieus[1:]
                for dieu in dieus:
                    dieu = dieu.strip()
                    results.append(
                        "Chương " + ten_chuong + ". Mục " + ten_muc + ". Điều " + dieu
                    )
        else:
            dieus = chuong.split("\n\nĐiều")
            ten_chuong = dieus[0].strip().replace("\n", " ").replace("  ", " ")
            dieus = dieus[1:]
            for dieu in dieus:
                dieu = dieu.strip()
                results.append("Chương " + ten_chuong + ". Điều " + dieu)
    print(f"Splited to {len(results)} chunks")
    return results


def convert_2_document(chunks: List[str], source: str) -> List[Document]:
    documents = []
    for chunk in chunks:
        while "\n\n" in chunk:
            chunk = chunk.replace("\n\n", "\n")
        document = Document(page_content=chunk, metadata={"source": source})
        documents.append(document)
    return documents


def save_2_pickle(documents: List[Document], file_path: str):
    with open(file_path, "wb") as file:
        pickle.dump(documents, file)


def load_data(file_path: str) -> List[Document]:
    with open(file_path, "rb") as file:
        documents = pickle.load(file)
    return documents


def prepare(file_path: str, source: str, file_destination_path: str):
    document = load_docx(file_path)
    print(f"Loaded data from {file_path}")
    splits = split_law_text(document[0].page_content)
    documents = convert_2_document(
        splits,
        source=source,
    )
    save_2_pickle(documents, file_path=file_destination_path)
    print(f"Saved to {file_destination_path}")


if __name__ == "__main__":
    prepare(
        file_path="/home/quangster/Workspace/Easy_Law/rag/data/Luật-42-2024-QH15.docx",
        source="https://luatvietnam.vn/lao-dong/bo-luat-lao-dong-2019-179015-d1.html",
        file_destination_path="./data/LuatDatDai2013.pkl",
    )
    documents = load_data("./data/LuatDatDai2013.pkl")
    print(documents[1].page_content)
