import os
from dotenv import load_dotenv

from pydantic import BaseModel
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from chain import BasicRAG, AdvanceRoutingRAG, AdvanceMultiQueryRAG
from retriever import get_retriever
from config import MULTI_VECTOR_DB

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

app = FastAPI()
embedding = HuggingFaceEmbeddings(model_name=os.environ["EMBEDDING_MODEL_NAME"])
retrievers = {}
for e in list(MULTI_VECTOR_DB.values()):
    retrievers[e] = get_retriever(source=e, embedding=embedding)
gg_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
gpt_llm = ChatOpenAI(temperature=0)

# basicrag = BasicRAG(retrievers["dan_su"], gpt_llm)
advancerag = AdvanceRoutingRAG(retrievers, gpt_llm)
# mutliqueryRag = AdvanceMultiQueryRAG(retrievers, gpt_llm)


print(advancerag.answer(question="Luật hôn nhân gia đình là gì ?"))
