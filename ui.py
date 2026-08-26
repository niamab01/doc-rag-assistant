import streamlit as st
import tempfile
import os
from app.ingestion import extract_text_from_pdf, chunk_documents
from app.vectorStoring import create_vectorstore
from app.ragChain import build_rag_chain

st.set_page_config(page_title="Doc Analyzer")
st.title("Document Analyzer")

# --- Sidebar : upload + processing ---
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    
    if st.button("Process Document") and uploaded_file:
        with st.spinner("Processing..."):
            # 1. Sauvegarder le fichier temporairement
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())  # écrire le contenu du fichier uploadé
                tmp_path = tmp.name
            
            # 2. Ingestion
            pages = extract_text_from_pdf(tmp_path)
            chunks = chunk_documents(pages)
            
            # 3. Vector store
            vectorstore = create_vectorstore(chunks)
            
            # 4. RAG chain
            st.session_state["chain"] = build_rag_chain(vectorstore,chunks)
            
            # 5. Nettoyage
            os.unlink(tmp_path)
            
            st.success(f"Done! {len(pages)} pages, {len(chunks)} chunks.")

# --- Chat interface ---
if "chain" not in st.session_state:
    st.info("Please upload and process a PDF to start chatting.")
else:
    question = st.chat_input("Ask a question about the document")
    if question:
        st.chat_message("user").write(question)
        with st.spinner("Thinking..."):
            response = st.session_state["chain"].invoke(question)
        st.chat_message("assistant").write(response)
