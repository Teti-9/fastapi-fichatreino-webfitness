from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.sqlalchemy.models import models

class RepositorioTreino():
    def __init__(self, session: Session):
        self.session = session
    
    def popular_db(self, treino: schemas.Treino):
        treino_db = models.Treino(
                                nome = treino.nome.capitalize(),
                                musculo = treino.musculo.capitalize(),
                                compativel = treino.compativel,)
        
        self.session.add(treino_db)
        self.session.commit()
        self.session.refresh(treino_db)
        return treino_db
    
    def procurar_exerc(self, tipo: str):
        procurar = select(models.Treino).where(and_(models.Treino.musculo == tipo)).order_by(func.random()).limit(1)
        return self.session.execute(procurar).scalars().first()