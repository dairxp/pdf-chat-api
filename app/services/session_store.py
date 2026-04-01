from langchain_community.vectorstores import FAISS


class SessionStore:
    """In-memory store for PDF sessions. Each session holds a vector store and chat history."""

    def __init__(self):
        self._sessions: dict[str, dict] = {}

    def create(self, session_id: str, vector_store: FAISS) -> None:
        self._sessions[session_id] = {"vector_store": vector_store, "history": []}

    def get(self, session_id: str) -> dict | None:
        return self._sessions.get(session_id)

    def add_to_history(self, session_id: str, human: str, ai: str) -> None:
        self._sessions[session_id]["history"].append({"human": human, "ai": ai})

    def delete(self, session_id: str) -> None:
        del self._sessions[session_id]

    def exists(self, session_id: str) -> bool:
        return session_id in self._sessions


session_store = SessionStore()
