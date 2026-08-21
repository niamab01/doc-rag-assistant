from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
def create_vectorstore(chunks: list, persist_directory: str = "./chroma_db"):
  embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
  vectorstore = Chroma.from_documents(chunks, embedding, persist_directory=persist_directory)
  return vectorstore

    
def load_vectorstore(persist_directory: str = "./chroma_db"):
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding )
    return vectorstore
