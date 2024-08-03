from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents import Document
import pickle
from typing import List
import os


def load_docx(file_path) -> List[Document]:
    """Load documents from file .docx"""
    loader = Docx2txtLoader(file_path)
    documents = loader.load()
    return documents


def split_law_text(text: str) -> List[str]:
    """Chia tài liệu thành các documents theo điều. Mỗi document là một điều"""
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

def split_law_text_by_dieu(text: str, link: str) -> List[Document]:
    dieus = text.split("\n\nĐiều")
    metadata = dieus[0].strip()
    dieus = dieus[1:]
    result = []
    for dieu in dieus:
        dieu = dieu.strip()
        result.append(
            Document(page_content="Điều " + dieu, metadata={"source": metadata, "link": link})
        )
    return result


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


def prepare_data(file_path: str, source: str) -> List[Document]:
    document = load_docx(file_path)
    print(f"Loaded data from {file_path}")
    splits = split_law_text(document[0].page_content)
    documents = convert_2_document(
        splits,
        source=source,
    )
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
    document = load_docx("./data/dan_su/91-2015-QH13.docx")
    documents = split_law_text_by_dieu(
        document[0].page_content,
        link="https://luatvietnam.vn/dan-su/bo-luat-dan-su-2015-moi-nhat-so-91-2015-qh13-101333-d1.html",
    )
    save_2_pickle(documents, "./datapickle/dan_su/91-2015-QH13.pkl")
    print(documents[0])