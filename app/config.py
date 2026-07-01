from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cors_origins: List[str]

    db_host: str
    db_username: str
    db_database: str
    db_password: str

    redis_host: str
    redis_port: int
    redis_ttl_mins: int

    resend_api_key: str
    email_receiver: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
