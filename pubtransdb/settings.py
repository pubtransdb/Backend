from pydantic import BaseSettings, Field, PostgresDsn

from pubtransdb import __version__


class Settings(BaseSettings):
    title: str = "pubtransdb"
    description: str = ""
    version: str = __version__
    debug: bool = False
    postgres_dsn: PostgresDsn = Field(default=...)

    class Config:
        env_file = ".env"


settings = Settings()
