import json
import os
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def sanitize_metadata(metadata: dict):
    for key, value in metadata.items():
        if isinstance(value, list):
            metadata[key] = ", ".join(map(str, value))
        elif isinstance(value, dict):
            metadata[key] = ", ".join(f"{k}: {v}" for k, v in value.items())
    return metadata

def create_vectorstore(persist_dir="chroma_db/"):
    model = "sentence-transformers/paraphrase-MiniLM-L3-v2"
    hf_embedding_model = HuggingFaceEmbeddings(model_name=model)
    
    try:
        with open("data/ds.json", "r") as f:
            raw_data = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to read JSON data: {e}")
    
    try:
        documents = [
            Document(
                page_content=row["content"],
                metadata={"category": row["category"], **sanitize_metadata(row["metadata"])},
            )
            for row in raw_data
        ]
    except Exception as e:
        raise RuntimeError(f"Failed to create documents: {e}")
    
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=hf_embedding_model,
        persist_directory=persist_dir,
        collection_name="my_collection",
    )
    return vector_store.as_retriever(search_kwargs={"k": 2})

def load_vectorstore(persist_dir="chroma_db/"):
    model = "sentence-transformers/paraphrase-MiniLM-L3-v2"
    hf_embedding_model = HuggingFaceEmbeddings(model_name=model)
    
    if os.path.exists(persist_dir) and os.path.exists(os.path.join(persist_dir, "chroma.sqlite3")):
        print("Loading existing vector store from disk...")
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=hf_embedding_model,
            collection_name="my_collection"
        ).as_retriever(search_kwargs={"k": 2})
    
    print("Creating new vector store...")
    return create_vectorstore(persist_dir)