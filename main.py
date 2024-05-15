from typing  import Dict, List, Optional
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status, Path
from fastapi.responses import JSONResponse, Response

from models import Curso

app = FastAPI(
  title= 'API de Cursos',
  version= '0.0.1',
  description= 'API para estudo do FastAPI'
  )

cursos = {
  1: {
    "titulo" : "Formação QA Engineer",
    "aulas": 90,
    "horas": 180,
  },
  2: {
    "titulo" : "Automação de testes full stack",
    "aulas": 50,
    "horas": 120,
  }   
}

@app.get('/cursos', description= 'Retorna todos os cursos ou uma lista vazia', summary='Buscar todos os cursos', response_description='Cursos encontrados com sucesso')
async def get_cursos():
  return cursos

@app.get('/cursos/{curso_id}', description= 'Retorna um curso pelo id', summary='Buscar curso por ID')
async def get_curso(curso_id: int = Path(title='ID do curso', description='Deve ser entre 1 e 2', gt=0, lt=3)):
  try:
    curso = cursos[curso_id]
    return curso
  except KeyError:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado!')

@app.post('/cursos', status_code=status.HTTP_201_CREATED, description= 'Criar um novo curso', summary='Criar um novo curso', response_model=Curso)
async def post_curso(curso: Curso):
  next_id: int = len(cursos) + 1  
  cursos[next_id] = curso
  del curso.id
  return curso

@app.put('/cursos/{curso_id}', description= 'Alterar informações do curso', summary='Alterar informações de curso')
async def put_curso(curso_id: int, curso: Curso):
  if curso_id in cursos:
    cursos[curso_id] = curso
    del curso.id
        
    return curso
  else:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail= f'Não existe um curso com o ID {curso_id}')
  
@app.delete('/cursos/{curso_id}', description= 'Excluir um curso', summary='Excluir curso por ID')
async def delete_curso(curso_id: int):
  if curso_id in cursos:
    del cursos[curso_id]
    #return JSONResponse(status_code=status.HTTP_204_NO_CONTENT) -> bug fastapi
    return Response(status_code=status.HTTP_204_NO_CONTENT)
  else:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail= f'Não existe um curso com ID {curso_id}')

  
if __name__ == '__main__':
  import uvicorn
  
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
  