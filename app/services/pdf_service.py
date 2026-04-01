import fitz  # PyMuPDF
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings


def extract_documents(pdf_bytes: bytes) -> tuple[list[Document], int]:
    """Extract text from PDF bytes, return LangChain Documents and page count."""
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    page_count = len(pdf)
    documents = []

    for page_num, page in enumerate(pdf, start=1):
        text = page.get_text().strip()
        if text:
            documents.append(
                Document(
                    page_content=text,
                    metadata={"page": page_num},
                )
            )

    pdf.close()
    return documents, page_count


def build_vector_store(documents: list[Document]) -> FAISS:
    """Split documents and build a FAISS vector store."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    vector_store = FAISS.from_documents(chunks, embeddings)

    return vector_store
