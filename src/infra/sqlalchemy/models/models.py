from sqlalchemy import Column, Integer, String
from src.infra.sqlalchemy.config.database import Base

class Treino(Base):
    __tablename__ = 'ficha'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(30), nullable=False)
    musculo = Column(String(30), nullable=False)
    compativel = Column(Integer, nullable=False)