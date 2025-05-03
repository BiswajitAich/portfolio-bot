import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

def getLLM():
    load_dotenv()
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if GROQ_API_KEY is None:
        raise EnvironmentError("GROQ_API_KEY not found in environment variables.")
    
    return ChatGroq(
        temperature=0,
        groq_api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192",  
        max_tokens=512,
    )