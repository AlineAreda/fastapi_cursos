from typing import Optional
from pydantic import BaseModel, validator

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    # O validador é definido como um método de classe dentro da classe Curso
    @validator('titulo')
    def validar_titulo(cls, value):
        words = value.split(' ')
        if len(words) < 2:
            raise ValueError('O título deve ter pelo menos 3 palavras')
          
        if value.islower():
          raise ValueError('O título deve ser capitalizado')
        
        return value
