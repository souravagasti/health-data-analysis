from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration object.
    Reads from .env and provides typed attributes.
    """

    # Tell Pydantic to load from .env at project root
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Postgres ---
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"   # optional override, default = local
    POSTGRES_PORT: int = 5432

    @property
    def pg_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # --- Metabase ---
    MB_DB_TYPE: str = "postgres"
    MB_DB_HOST: str = "postgres"
    MB_DB_PORT: int = 5432
    MB_DB_USER: str | None = None
    MB_DB_PASS: str | None = None
    MB_DB_DBNAME: str | None = None
    MB_ENCRYPTION_SECRET: str | None = None

    # --- Other configs (future: OpenAI API keys, etc.) ---
    OPENAI_API_KEY: str | None = None


# Cache the settings object so it’s loaded once
@lru_cache
def get_settings() -> Settings:
    return Settings()


if __name__ == "__main__":
    settings = get_settings()
    print("Postgres URL (masked):", settings.pg_url.replace(settings.POSTGRES_PASSWORD, "*****"))
    print("Metabase DB:", settings.MB_DB_DBNAME)
