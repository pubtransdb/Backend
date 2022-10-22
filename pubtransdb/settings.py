from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    debug: bool = False
    postgres_dsn: PostgresDsn = Field(default=...)

    class Config:
        env_file = ".env"


settings = Settings()
