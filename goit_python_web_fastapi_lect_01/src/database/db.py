from configparser import ConfigParser
from pathlib import Path
from fastapi import HTTPException, status

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


CONFIG_FILE = Path(__file__).resolve().parent.parent.joinpath("conf/config.ini")
config = ConfigParser()
URI = None
if CONFIG_FILE.exists():
    config.read(CONFIG_FILE)
    username = config.get('DEV_DB', 'USERNAME')
    password = config.get('DEV_DB', 'PASSWORD')
    domain = config.get('DEV_DB', 'DOMAIN')
    port = config.get('DEV_DB', 'PORT')
    database = config.get('DEV_DB', 'DATABASE')

    URI = f"postgresql+psycopg2://{username}:{password}@{domain}:{port}/{database}"

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = URI


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
        print(err)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) 
    finally:
        db.close()