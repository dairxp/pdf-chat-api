from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    llm_provider: str = "groq"
    llm_model: str = "llama-3.1-8b-instant"

    groq_api_key: str = ""
    openai_api_key: str = ""
    gemini_api_key: str = ""

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    max_pdf_size_mb: int = 20


settings = Settings()
