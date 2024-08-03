import os
from dotenv import load_dotenv

from pydantic import BaseModel
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from chain import BasicRAG, AdvanceRAG
from retriever import get_retriever
from config import MULTI_VECTOR_DB

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()


app = FastAPI()
embedding = HuggingFaceEmbeddings(model_name=os.environ["EMBEDDING_MODEL_NAME"])
retrievers = {}
for e in list(MULTI_VECTOR_DB.values()):
    retrievers[e] = get_retriever(source=e, embedding=embedding)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
gpt_llm = ChatOpenAI(temperature=0)

basicrag = BasicRAG(retrievers["test"], llm)
advancerag = AdvanceRAG(retrievers, gpt_llm)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/")
async def home_route():
    return {"message": "LAW RAG API"}

@app.post("/v1/rag")
async def rag_route(question: Question):
    print(question)
    return {"answer": basicrag.answer(question.question)}


@app.post("/v2/rag")
async def rag_route(question: Question):
    print(question)
    return {"answer": advancerag.answer(question.question)}


if __name__ == "__main__":
    import uvicorn
    from pyngrok import ngrok
    import nest_asyncio

    ngrok.set_auth_token(os.environ["NGROK_AUTH_TOKEN"])
    PORT = int(os.environ["SERVER_PORT"])
    ngrok_tunnel = ngrok.connect(PORT, domain=os.environ["NGROK_STATIC_DOMAIN"])
    print("Public URL: ", ngrok_tunnel.public_url)
    nest_asyncio.apply()
    uvicorn.run("server:app", reload=True, port=PORT)
