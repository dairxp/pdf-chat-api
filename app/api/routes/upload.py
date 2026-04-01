import uuid

from fastapi import APIRouter, HTTPException, UploadFile, File

from app.core.config import settings
from app.models.schemas import UploadResponse
from app.services.pdf_service import extract_documents, build_vector_store
from app.api.routes.chat import sessions

router = APIRouter()

MAX_BYTES = settings.max_pdf_size_mb * 1024 * 1024


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    pdf_bytes = await file.read()

    if len(pdf_bytes) > MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the {settings.max_pdf_size_mb} MB limit.",
        )

    documents, page_count = extract_documents(pdf_bytes)

    if not documents:
        raise HTTPException(status_code=422, detail="Could not extract text from PDF.")

    vector_store = build_vector_store(documents)
    session_id = str(uuid.uuid4())
    sessions[session_id] = vector_store

    return UploadResponse(
        session_id=session_id,
        pages=page_count,
        message="PDF processed. You can start chatting.",
    )
