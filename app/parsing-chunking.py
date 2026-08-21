import fitz
def extract_text_from_pdf(pdf_path):
  pdf_doc = fitz.open(pdf_path)
  extracted = []
  for page_num in range(pdf_doc.page_count()):
    page = pdf_doc.load_page(page_num)
    extracted.append(page.get_text())
  return extracted

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
def chunk_documents(pages, chunk_size: int = 1000, chunk_overlap: int = 200):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunkoverlap)

  metadatas = [{"page": i+1} for i in range(len(pages))]

  documents = text_splitter.create_documents(pages, metadatas=metadatas)
  return documents

