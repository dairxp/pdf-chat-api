# pdf-chat-api

REST API to ask questions to any PDF in natural language.

Upload a PDF, get a session ID, and start chatting. Built with FastAPI, LangChain, FAISS, and Groq — but the LLM provider can be swapped for OpenAI, Gemini, or any LangChain-compatible model by changing two lines in `.env`.

---

## Stack

- **FastAPI** — REST API framework
- **LangChain** — LLM orchestration
- **Groq / OpenAI / Gemini** — LLM provider (configurable)
- **FAISS** — local vector store, no server needed
- **HuggingFace Embeddings** — free, runs locally
- **PyMuPDF** — PDF text extraction

---

## Quickstart

```bash
git clone https://github.com/dairxp/pdf-chat-api
cd pdf-chat-api
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # fill in your API key
uvicorn app.main:app --reload
```

Docs available at `http://localhost:8000/docs`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload a PDF, returns `session_id` |
| POST | `/chat/{session_id}` | Ask a question about the uploaded PDF |
| DELETE | `/session/{session_id}` | Clear session from memory |

### Upload PDF

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"
```

```json
{ "session_id": "abc123", "pages": 12, "message": "PDF ready. Start chatting." }
```

### Ask a question

```bash
curl -X POST http://localhost:8000/chat/abc123 \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

```json
{ "answer": "...", "sources": [1, 3] }
```

---

## Switching LLM provider

In `.env`, change the provider and model:

```env
# Groq (default)
LLM_PROVIDER=groq
LLM_MODEL=llama-3.1-8b-instant
GROQ_API_KEY=your_key

# OpenAI
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
OPENAI_API_KEY=your_key
```

No code changes needed.

---

## Project structure

```
pdf-chat-api/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── api/routes/          # upload, chat endpoints
│   ├── core/config.py       # settings via pydantic-settings
│   ├── services/            # PDF processing, chat logic
│   └── models/schemas.py    # Pydantic request/response models
├── tests/
├── .env.example
├── Dockerfile
└── requirements.txt
```

---

> Published by [dairxp](https://github.com/dairxp)
