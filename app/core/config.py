from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EastAdvantage Address Book Service"
    DATABASE_URL: str = "sqlite:///.address_book.db"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()
