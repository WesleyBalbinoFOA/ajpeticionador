# backend/core/config.py
# Lê todas as variáveis do .env e disponibiliza tipadas

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # IA
    gemini_api_key: str
    groq_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    groq_model: str = "llama-3.3-70b-versatile"
    max_tokens: int = 4096
    temperatura: float = 0.3

    # Backend
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    environment: str = "development"
    secret_key: str = "dev-secret-troque-em-producao"

    # CORS
    allowed_origins: str = "http://localhost:5173"

    # Upload
    max_upload_mb: int = 10
    allowed_extensions: str = "xlsx,xls,png,jpg,jpeg,pdf"

    # Modelos
    modelos_path: str = "./modelos"

    # Supabase (opcional)
    supabase_url: str = ""
    supabase_key: str = ""

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    @property
    def extensions_list(self) -> list[str]:
        return [e.strip() for e in self.allowed_extensions.split(",")]

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Singleton — lê .env uma vez e cacheia."""
    return Settings()
