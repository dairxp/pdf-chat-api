from fastapi import APIRouter, HTTPException
from langchain_community.vectorstores import FAISS

from app.models.schemas import ChatRequest, ChatResponse, DeleteResponse
from app.services.chat_service import answer_question

router = APIRouter()

# In-memory session store: session_id -> FAISS vector store
sessions: dict[str, FAISS] = {}


@router.post("/chat/{session_id}", response_model=ChatResponse)
async def chat(session_id: str, body: ChatRequest):
    vector_store = sessions.get(session_id)

    if vector_store is None:
        raise HTTPException(status_code=404, detail="Session not found. Upload a PDF first.")

    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    result = answer_question(vector_store, body.question)

    return ChatResponse(answer=result["answer"], sources=result["sources"])


@router.delete("/session/{session_id}", response_model=DeleteResponse)
async def delete_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found.")

    del sessions[session_id]

    return DeleteResponse(message="Session deleted.")
