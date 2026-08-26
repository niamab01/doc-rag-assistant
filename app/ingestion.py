import fitz
#détection de la bordure pour éviter des résultats faussés par la répétition des informations sur le coté d'un document
def detect_repeated_content(pages: list[str], threshold: float = 0.3) -> set:
    line_counter = Counter()
    for page in pages:
        unique_lines = set(page.split('\n'))
        for line in unique_lines:
            stripped = line.strip()
            if len(stripped) > 2:
                line_counter[stripped] += 1
    
    num_pages = len(pages)
    repeated = set()
    for line, count in line_counter.items():
        if count > num_pages * threshold:
            repeated.add(line)
    return repeated

def clean_page_text(text: str, repeated_lines: set) -> str:
    lines = text.split('\n')
    cleaned = [line for line in lines 
               if line.strip() not in repeated_lines 
               and len(line.split()) >= 3]
    return '\n'.join(cleaned)

def extract_text_from_pdf(pdf_path):
  pdf_doc = fitz.open(pdf_path)
  raw_pages = []
  for page in pdf_doc:
      raw_pages.append(page.get_text())
  repeated = detect_repeated_content(raw_pages)
  extracted = []
  for page_num in range(pdf_doc.page_count()):
    text = clean_page_text(raw_pages[page_num], repeated)
    page = pdf_doc.load_page(page_num)
    finder = page.find_tables()
        for tab in finder.tables:
            df = tab.to_pandas()
            text += "\n\nTABLE:\n" + df.to_string()
        
        extracted.append(text)
  return extracted

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
def chunk_documents(pages, chunk_size: int = 1000, chunk_overlap: int = 200):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunkoverlap)

  metadatas = [{"page": i+1} for i in range(len(pages))]

  documents = text_splitter.create_documents(pages,metadatas=metadatas)
  documents = [doc for doc in documents if len(doc.page_content.split()) >= 20]
  return documents

