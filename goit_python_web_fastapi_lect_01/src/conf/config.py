from os import environ
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(BASE_PATH.joinpath(".env"))
APP_ENV = environ.get("APP_ENV")
#print(APP_ENV)

# SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USERNAME}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}

class Settings(BaseSettings):
    sqlalchemy_database_url: str | None = None
    token_secret_key: str = "some_SuPeR_key"
    token_algorithm: str = "HS256"
    mail_username: str = "user@example.com"
    mail_password: str = ""
    mail_from: str = "user@example.com"
    mail_port: int = 465
    mail_server: str = ""
    mail_from_name: str = ""
    redis_host: str = "localhost"
    redis_port: int = 6379

    class Config:
        extra = "ignore"
        # TESTED FIRST USED ENV variables, even if file defined.
        env_file = BASE_PATH.joinpath(f".env-{APP_ENV}") if APP_ENV else BASE_PATH.joinpath(".env")
        env_file_encoding = "utf-8"


settings = Settings()

if __name__ == "__main__":
    print(settings.Config.env_file)
    print(settings)
