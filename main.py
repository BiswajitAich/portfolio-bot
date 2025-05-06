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


@app.get("/health")
async def health():
    try:
        _ = app.state.chain
        return {"status": "ok"}
    except AttributeError:
        raise HTTPException(status_code=503, detail="Backend is loading")


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        if hasattr(app.state.chain, "ainvoke"):
            result = await app.state.chain.ainvoke({"question": request.question})
        else:
            result = app.state.chain.invoke({"question": request.question})
        return {"answer": result}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


@app.get("/vector-store-rerun")
async def vector_store_rerun():
    try:
        if os.getenv("APP_ENV", "") == "development":
            create_vectorstore()
            return {
                "env": "development",
                "message": "Vector store successfully created!",
            }
        else:
            return {"env": "not development"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


@app.get("/test")
async def test():
    try:
        if os.getenv("APP_ENV", "") == "development":
            retriever = load_vectorstore()
            prompt_template = getPromptTemplate()
            # data = await chain.ainvoke("what is biswajit's height?")
            context = await retriever.ainvoke("what is biswajit's height?")
            # data = await prompt_template.ainvoke({
            #     "question": "what is biswajit's height?",
            #     "context": context
            # })
            return {
                "env": "development",
                "data": context,
            }
        else:
            return {"env": "not development"}
    except Exception as e:
        return {"error": str(e)}


def main():
    print("Hello from portfolio-bot!")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
