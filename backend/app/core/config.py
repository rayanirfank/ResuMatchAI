from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./resumatch.db"
    ADZUNA_APP_ID: str = "0b7e6266"
    ADZUNA_APP_KEY: str = "b26cfc1fe8b398176d7466875f0ce53b"

    class Config:
        env_file = ".env"


settings = Settings()