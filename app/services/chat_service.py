import json
from typing import AsyncGenerator

from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.services.llm_factory import get_llm


def answer_question(vector_store: FAISS, question: str, history: list[dict]) -> dict:
    """QA chain with chat history. Returns answer and source pages."""
    llm = get_llm()

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True,
    )

    chat_history = [(h["human"], h["ai"]) for h in history]
    result = chain.invoke({"question": question, "chat_history": chat_history})

    source_pages = sorted({doc.metadata["page"] for doc in result["source_documents"]})

    return {"answer": result["answer"], "sources": source_pages}


async def stream_answer(
    vector_store: FAISS, question: str, history: list[dict]
) -> AsyncGenerator[str, None]:
    """Stream answer token by token using SSE format.

    Yields:
        SSE-formatted strings. Last event contains source pages.
    """
    docs = vector_store.similarity_search(question, k=4)
    context = "\n\n".join(doc.page_content for doc in docs)
    source_pages = sorted({doc.metadata["page"] for doc in docs})

    messages = [
        SystemMessage(
            content=(
                "You are a helpful assistant. Answer the question using only the "
                "context below. If the answer is not in the context, say so clearly.\n\n"
                f"Context:\n{context}"
            )
        )
    ]
    for h in history:
        messages.append(HumanMessage(content=h["human"]))
        messages.append(AIMessage(content=h["ai"]))
    messages.append(HumanMessage(content=question))

    llm = get_llm()
    full_answer = []

    async for chunk in llm.astream(messages):
        token = chunk.content
        if token:
            full_answer.append(token)
            yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"

    yield f"data: {json.dumps({'type': 'sources', 'pages': source_pages})}\n\n"
    yield "data: [DONE]\n\n"
