from configparser import ConfigParser
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

    URI = f"postgresql://{username}:{password}@{domain}:{port}/{database}"

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = URI

print(SQLALCHEMY_DATABASE_URL)
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()
    
# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()