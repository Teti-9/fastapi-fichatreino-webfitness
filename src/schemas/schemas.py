from pydantic import ConfigDict, BaseModel
from typing import Optional

class Treino(BaseModel):
    id: Optional[int] = None
    nome: str
    musculo: str
    compativel: int

    model_config = ConfigDict(from_attributes=True)