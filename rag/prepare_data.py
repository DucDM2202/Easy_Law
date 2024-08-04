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


def prepare(file_path: str, link: str, file_destination_path: str):
    document = load_docx(file_path)
    print(f"Loaded data from {file_path}")
    documents = split_law_text_by_dieu(
        document[0].page_content,
        link=link,
    )
    print(f"Split ino {len(documents)} chunks")
    save_2_pickle(documents, file_path=file_destination_path)
    print(f"Saved to {file_destination_path}")

def prepare_all():
    # dan su
    prepare(
        "./data/dan_su/91-2015-QH13.docx",
        "https://luatvietnam.vn/dan-su/bo-luat-dan-su-2015-moi-nhat-so-91-2015-qh13-101333-d1.html",
        "./datapickle/dan_su/91-2015-QH13.pkl",
    )
    # dat dai
    prepare(
        "./data/dat_dai/45_2013_QH13.docx",
        "https://luatvietnam.vn/dat-dai/luat-dat-dai-cua-quoc-hoi-so-45-2013-qh13-83386-d1.html",
        "./datapickle/dat_dai/45_2013_QH13.pkl",
    )
    # hien phap
    prepare(
        "./data/hien_phap/HienPhap2013.docx",
        "https://luatvietnam.vn/tu-phap/hien-phap-18-2013-l-ctn-quoc-hoi-83320-d1.html",
        "./datapickle/hien_phap/HienPhap2013.pkl",
    )
    # tai chinh
    prepare(
        "./data/tai_chinh/46-2010-QH12.docx",
        "https://luatvietnam.vn/tai-chinh/luat-ngan-hang-nha-nuoc-2010-53469-d1.html",
        "./datapickle/tai_chinh/46-2010-QH12.pkl",
    )
    prepare(
        "./data/tai_chinh/61_2020_QH14.docx",
        "https://luatvietnam.vn/dau-tu/luat-dau-tu-2020-186270-d1.html",
        "./datapickle/tai_chinh/61_2020_QH14.pkl",
    )
    prepare(
        "./data/tai_chinh/88_2015_QH13.docx",
        "https://luatvietnam.vn/ke-toan/luat-ke-toan-2015-101336-d1.html",
        "./datapickle/tai_chinh/88_2015_QH13.pkl",
    )
    prepare(
        "./data/tai_chinh/97_2015_QH13.docx",
        "https://luatvietnam.vn/thue/luat-phi-va-le-phi-2015-101327-d1.html",
        "./datapickle/tai_chinh/97_2015_QH13.pkl",
    )
    # lao dong
    prepare(
        "./data/lao_dong/45-2019-QH14.docx",
        "https://luatvietnam.vn/lao-dong/bo-luat-lao-dong-2019-179015-d1.html",
        "./datapickle/lao_dong/45-2019-QH14.pkl",
    )
    prepare(
        "./data/lao_dong/69-2020-QH14.docx",
        "https://luatvietnam.vn/lao-dong/luat-nguoi-lao-dong-viet-nam-di-lam-viec-o-nuoc-ngoai-theo-hop-dong-2020-195185-d1.html",
        "./datapickle/lao_dong/69-2020-QH14.pkl",
    )
    # hon nhan gia dinh
    prepare(
        "./data/hon_nhan_gia_dinh/52-2014-QH13.docx",
        "https://luatvietnam.vn/hon-nhan-gia-dinh/luat-hon-nhan-va-gia-dinh-2014-87930-d1.html",
        "./datapickle/hon_nhan_gia_dinh/52-2014-QH13.pkl",
    )

if __name__ == "__main__":
    prepare_all()
