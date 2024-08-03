from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

@app.get("/")
async def home():
    return {"message": "LAW RAG API"}


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
