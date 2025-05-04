from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap, RunnableLambda

def getChain(retriever, prompt_template, llm):
    # Step 1: Create retriever -> context retriever pipeline
    def format_docs(docs):
        return "\n\n".join([f"{doc.page_content}\n{doc.metadata}" for doc in docs])
    
    retriever_chain = RunnableLambda(lambda x: x["question"]) | retriever | format_docs
    
    # Step 2: Combine retriever + prompt_template
    return RunnableMap({
        "context": retriever_chain,
        "question": lambda x: x["question"]
    }) | prompt_template | llm | StrOutputParser()