from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Annotated
from fastapi import Depends

SQLACHEMY_DATABASE_URL = 'sqlite:///./workoutgen.db'

engine = create_engine(SQLACHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def gerar_db():
    Base.metadata.create_all(bind=engine)

def acessar_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

db_dependency = Annotated[Session, Depends(acessar_db)]