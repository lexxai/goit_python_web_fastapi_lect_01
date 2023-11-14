from configparser import ConfigParser
from os import environ
from pathlib import Path
from dotenv import load_dotenv
from fastapi import HTTPException, status

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


username = None
password = None
domain = None
port = None
database = None
URI = None 
domain = environ.get("POSTGRES_HOST")
if not domain:
    ENV_FILE = Path(__file__).resolve().parent.parent.parent.parent.joinpath(".env")
    load_dotenv(ENV_FILE)
    domain = environ.get("POSTGRES_HOST")
    # print(f"{ENV_FILE=} {domain=}")

    username = environ.get("POSTGRES_USERNAME")
    password = environ.get("POSTGRES_PASSWORD")
    domain = environ.get("POSTGRES_HOST")
    port = environ.get("POSTGRES_PORT")
    database = environ.get("POSTGRES_DB")
if not domain:
    CONFIG_FILE = Path(__file__).resolve().parent.parent.joinpath("conf/config.ini")
    if CONFIG_FILE.exists():
        config = ConfigParser()
        config.read(CONFIG_FILE)
        username = config.get('DEV_DB', 'USERNAME')
        password = config.get('DEV_DB', 'PASSWORD')
        domain = config.get('DEV_DB', 'DOMAIN')
        port = config.get('DEV_DB', 'PORT')
        database = config.get('DEV_DB', 'DATABASE')
if domain and port:
    URI = f"postgresql+psycopg2://{username}:{password}@{domain}:{port}/{database}"

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = URI

assert SQLALCHEMY_DATABASE_URL is not None, "SQLALCHEMY_DATABASE_URL UNDEFINED"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True  
)

DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
    
# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        print("SQLAlchemyError:", err)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) 
    finally:
        db.close()