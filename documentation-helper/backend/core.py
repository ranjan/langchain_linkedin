from dotenv import load_dotenv

load_dotenv()
from typing import Any, Dict, List
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
#from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from consts import INDEX_NAME
from langchain_community.llms import Ollama
from langchain_ollama import OllamaEmbeddings


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = OllamaEmbeddings(
        base_url="http://192.168.1.17:11434",  # Your local Ollama server
        model="nomic-embed-text"  # or "mxbai-embed-large"
    )
    chat = Ollama(model="llama3", base_url="http://192.168.1.17:11434", verbose=True, temperature=0)

    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)

    history_aware_retriever = create_history_aware_retriever(
        llm=chat, retriever=docsearch.as_retriever(), prompt=rephrase_prompt
    )
    qa = create_retrieval_chain(
        retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
    )

    result = qa.invoke(input={"input": query, "chat_history": chat_history})
    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"]
    }
    return new_result

if __name__ == "__main__":
    res = run_llm(query="What is langchain chain?")
    print(res["result"])
