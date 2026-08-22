from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

RAG_PROMPT_TEMPLATE = """You are a financial document analyst. 
    Answer the question based ONLY on the following context extracted from a financial report.
    If the answer is not in the context, say "I cannot find this information in the document."

    Context:
    {context}

    Question: {question}

    Answer:"""
def build_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    temperature=0.1)
    prompt = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()
    return chain
