from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()


def get_openai_embedding(model_name="text-embedding-3-small"):
    return OpenAIEmbeddings(model=model_name)


def get_huggingface_embedding(model_name=os.environ["EMBEDDING_MODEL_NAME"]):
    print(f"Loading model embedding {model_name}")
    return HuggingFaceEmbeddings(model_name=model_name)
