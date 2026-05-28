# backend/core/supabase.py

from supabase import create_client, Client
from core.config import get_settings
from functools import lru_cache


@lru_cache()
def get_supabase() -> Client:
    settings = get_settings()
    url = settings.supabase_url
    key = settings.supabase_key_efetiva
    if not url or not key:
        raise RuntimeError("SUPABASE_URL e SUPABASE_KEY (ou ANON_KEY) são obrigatórios.")
    return create_client(url, key)