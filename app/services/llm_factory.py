from langchain_core.language_models import BaseChatModel

from app.core.config import settings


def get_llm() -> BaseChatModel:
    """Return the configured LLM. Change provider in .env — no code changes needed."""
    provider = settings.llm_provider.lower()

    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(api_key=settings.groq_api_key, model=settings.llm_model)

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(api_key=settings.openai_api_key, model=settings.llm_model)

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            google_api_key=settings.gemini_api_key, model=settings.llm_model
        )

    raise ValueError(f"Unsupported LLM provider: '{provider}'. Use groq, openai, or gemini.")
