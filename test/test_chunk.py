from dotenv import load_dotenv
load_dotenv()
from app.ingestion import extract_text_from_pdf, chunk_documents
from app.vectorStoring import create_vectorstore

pages = extract_text_from_pdf("data/_R2_WEB_rapport_annuel_2025_0326_BGLBNPP.pdf")
chunks = chunk_documents(pages)
vectorstore = create_vectorstore(chunks)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

results = retriever.invoke("Quel est le résultat avant impôt en 2025 ?")
for i, doc in enumerate(results):
    print(f"\n--- Chunk {i+1} (page {doc.metadata.get('page')}) ---")
    print(doc.page_content[:300])
# Teste avec le vocabulaire exact du document
queries = [
    "Quel est le résultat avant impôt en 2025 ?",
    "COMPTE DE RÉSULTAT",
    "Résultat avant impôt Impôt sur les bénéfices",
]

for q in queries:
    print(f"\n=== Query: {q} ===")
    results = retriever.invoke(q)
    for i, doc in enumerate(results):
        print(f"Chunk (page {doc.metadata.get('page')}): {doc.page_content[:100]}")
# Compter les chunks par page pour les pages clés
pages_cles = [33, 34, 35, 36, 109]
for p in pages_cles:
    count = len([c for c in chunks if c.metadata.get("page") == p])
    if count > 0:
        print(f"\nPage {p} : {count} chunks")
        for c in chunks:
            if c.metadata.get("page") == p:
                print(f"  -> {c.page_content[:150]}")
