from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EastAdvantage Address Book Service"
    PROJECT_DESCRIPTION: str = "A simple address book API built with FastAPI and SQLAlchemy"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./address_book.db"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()
