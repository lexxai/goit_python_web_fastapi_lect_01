from os import environ

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
APP_ENV = environ.get("APP_ENV")

class Settings(BaseSettings):
    sqlalchemy_database_url: str = environ.get("SQLALCHEMY_DATABASE_URL", "")
    token_secret_key: str = environ.get("TOKEN_SECRET_KEY", "")
    token_algorithm: str = environ.get("TOKEN_ALGORITHM", "")
    mail_username: str = environ.get("MAIL_USERNAME", "")
    mail_password: str = environ.get("MAIL_PASSWORD", "")
    mail_from: str = environ.get("MAIL_FROM", "")
    mail_port: int =  int(environ.get("MAIL_PORT", 465))
    mail_server: str = environ.get("MAIL_SERVER", "")
    redis_host: str =  environ.get("REDIS_HOST", "localhost")
    redis_port: int =  int(environ.get("REDIS_PORT", 6379))

    class Config:
        env_file = f".env-{APP_ENV}" if APP_ENV else ".env"
        env_file_encoding = "utf-8"


settings = Settings()