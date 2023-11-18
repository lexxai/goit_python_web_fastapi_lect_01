from fastapi import HTTPException, status

from src.conf.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# URI = f"postgresql+psycopg2://{username}:{password}@{domain}:{port}/{database}"
# URI = "sqlite:///./sql_app.db"

URI = settings.sqlalchemy_database_url 
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