from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatRequest, ChatResponse, DeleteResponse
from app.services.chat_service import answer_question, stream_answer
from app.services.session_store import session_store

router = APIRouter()


@router.post("/chat/{session_id}", response_model=ChatResponse)
async def chat(session_id: str, body: ChatRequest):
    session = session_store.get(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found. Upload a PDF first.")

    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    result = answer_question(session["vector_store"], body.question, session["history"])

    session_store.add_to_history(session_id, body.question, result["answer"])

    return ChatResponse(answer=result["answer"], sources=result["sources"])


@router.post("/chat/{session_id}/stream")
async def chat_stream(session_id: str, body: ChatRequest):
    """Stream the answer token by token (Server-Sent Events).

    Use with: curl -N -X POST .../chat/{id}/stream -d '{"question": "..."}' -H 'Content-Type: application/json'
    """
    session = session_store.get(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found. Upload a PDF first.")

    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    history = session["history"]
    vector_store = session["vector_store"]
    question = body.question

    async def generate():
        collected_tokens = []
        async for event in stream_answer(vector_store, question, history):
            if "[DONE]" not in event and '"type": "sources"' not in event:
                import json
                data = json.loads(event.replace("data: ", "").strip())
                if data.get("type") == "token":
                    collected_tokens.append(data["content"])
            yield event

        full_answer = "".join(collected_tokens)
        if full_answer:
            session_store.add_to_history(session_id, question, full_answer)

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.delete("/session/{session_id}", response_model=DeleteResponse)
async def delete_session(session_id: str):
    if not session_store.exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found.")

    session_store.delete(session_id)

    return DeleteResponse(message="Session deleted.")
