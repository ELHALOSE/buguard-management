from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    
    OPENAI_API_KEY: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    GOOGLE_API_KEY: str

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()