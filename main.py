from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import uvicorn
import os
from utils.getDoc import load_vectorstore, create_vectorstore
from utils.getPrompt import getPromptTemplate
from utils.getLLM import getLLM
from utils.getChain import getChain
from pydantic import BaseModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    retriever = load_vectorstore()
    prompt_template = getPromptTemplate()
    llm = getLLM()
    app.state.chain = getChain(retriever, prompt_template, llm)
    yield


app = FastAPI(title="Portfolio Bot API", lifespan=lifespan)

class ChatRequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "portfolio-bot is live!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        result = app.state.chain.invoke({"question": request.question})
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/vector-store-rerun")
async def vector_store_rerun():
    try:
        create_vectorstore()
        return {"message": "Vector store successfully created!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

def main():
    print("Hello from portfolio-bot!")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
