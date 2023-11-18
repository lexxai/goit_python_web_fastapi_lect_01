from os import environ
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(Path(__file__).resolve().parent.parent.parent.parent.joinpath(".env"))
APP_ENV = environ.get("APP_ENV")

class Settings(BaseSettings):
    sqlalchemy_database_url: str = ""
    token_secret_key: str = "some_SuPeR_key"
    token_algorithm: str = "HS256"
    mail_username: str = ""
    mail_password: str = ""
    mail_from: str = ""
    mail_port: int = 465
    mail_server: str = ""
    mail_from_name: str = ""
    redis_host: str = "localhost"
    redis_port: int = 6379

    class Config:
        extra = "ignore"
        # TESTED FIRST USED ENV variables, even if file defined.
        env_file = f".env-{APP_ENV}" if APP_ENV else ".env"
        env_file_encoding = "utf-8"


settings = Settings()


if __name__ == "__main__":
    print(settings)
