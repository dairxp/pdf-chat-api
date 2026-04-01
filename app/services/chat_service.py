from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS

from app.services.llm_factory import get_llm


def answer_question(vector_store: FAISS, question: str) -> dict:
    """Run a QA chain over the vector store and return the answer with source pages."""
    llm = get_llm()

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True,
    )

    result = chain.invoke({"query": question})

    source_pages = sorted(
        {doc.metadata["page"] for doc in result["source_documents"]}
    )

    return {
        "answer": result["result"],
        "sources": source_pages,
    }
