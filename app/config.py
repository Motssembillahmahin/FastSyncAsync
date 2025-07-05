from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My FastAPI Sync and Async App"
    debug: bool = False
    sync_database_url: str
    async_database_url: str

    class Config:
        env_file = ".env"


settings = Settings()
