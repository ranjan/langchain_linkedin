from dotenv import load_dotenv
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaEmbeddings
from consts import INDEX_NAME
load_dotenv()

def ingest_docs() -> None:
    loader = ReadTheDocsLoader(path="langchain-docs/langchain-docs/api.python.langchain.com/en/latest")
    raw_documents = loader.load()
    print(f"loaded {len(raw_documents) }documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
    )
    documents = text_splitter.split_documents(documents=raw_documents)
    print(f"Split into {len(documents)} chunks")

    for doc in documents:
        old_path = doc.metadata["source"]
        new_url = old_path.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print(f"Going to insert {len(documents)} to Pinecone")
    embeddings = OllamaEmbeddings(
        base_url="http://192.168.1.17:11434",  # Your local Ollama server
        model="nomic-embed-text"  # or "mxbai-embed-large"
    )
    #PineconeVectorStore.from_documents(documents, embeddings, index_name=INDEX_NAME)
    vectorstore = PineconeVectorStore.from_existing_index(index_name=INDEX_NAME, embedding=embeddings)

    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        vectorstore.add_documents(batch)
        print(f"Uploaded batch {i} to {i + len(batch)}")

    print("****** Added to Pinecone vectorstore vectors")

if __name__ == "__main__":
    ingest_docs()
