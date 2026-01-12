from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    LLM_MODEL: str = "gemini-2.0-flash"
    # Optional comma-separated fallback models (try in order) e.g. "gemini-1.5-mini,gemini-1.0"
    LLM_MODEL_FALLBACKS: str = ""

    model_config = {"env_file": ".env"}

settings = Settings()
