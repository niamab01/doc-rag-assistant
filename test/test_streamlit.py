from dotenv import load_dotenv
load_dotenv()
from app.ingestion import extract_text_from_pdf, chunk_documents
from app.vectorStoring import create_vectorstore
from app.ragChain import build_rag_chain

pages = extract_text_from_pdf("data/_R2_WEB_rapport_annuel_2025_0326_BGLBNPP.pdf")
chunks = chunk_documents(pages)
print(f"Chunks: {len(chunks)}")
vectorstore = create_vectorstore(chunks)
chain = build_rag_chain(vectorstore, chunks)

questions = [
    "Quel est le résultat avant impôt en 2025 ?",
    "Quel est le résultat net part du groupe en 2025 ?",
    "Quel est le total actif au 31 décembre 2025 ? ?",
]
for q in questions:
    print(f"\nQ: {q}")
    print(f"A: {chain.invoke(q)}")

from langchain_community.retrievers import BM25Retriever

vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
bm25_retriever = BM25Retriever.from_documents(chunks, k=5)

query = "Quel est le résultat avant impôt en 2025 ?"

print("=== BM25 ===")
for doc in bm25_retriever.invoke(query):
    print(f"Page {doc.metadata.get('page')}: {doc.page_content[:150]}")

print("\n=== VECTOR ===")
for doc in vector_retriever.invoke(query):
    print(f"Page {doc.metadata.get('page')}: {doc.page_content[:150]}")
