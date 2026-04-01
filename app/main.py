from fastapi import FastAPI

from app.api.routes import upload, chat

app = FastAPI(
    title="pdf-chat-api",
    description="Ask questions to any PDF in natural language.",
    version="1.0.0",
)

app.include_router(upload.router, tags=["PDF"])
app.include_router(chat.router, tags=["Chat"])


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
