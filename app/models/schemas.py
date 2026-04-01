from pydantic import BaseModel
from typing import List


class UploadResponse(BaseModel):
    session_id: str
    pages: int
    message: str


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[int]


class DeleteResponse(BaseModel):
    message: str
