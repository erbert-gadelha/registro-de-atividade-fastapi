from fastapi import APIRouter, Depends
import psycopg2
from sqlalchemy.orm import Session
from database import get_db
from models import Empresa, ObrigacaoAcessoria
from starlette.responses import JSONResponse
from schemas import EmpresaDTO, ObrigacaoAcessoria_RequestDTO, ObrigacaoAcessoria_ResponseDTO
import service


empresa = APIRouter(prefix="/empresa")
obrigacao_acessoria = APIRouter(prefix="/obrigacao-acessoria")



@empresa.post("/")
def criar_empresa(request:EmpresaDTO, db: Session = Depends(get_db)) -> JSONResponse:
    db_empresa = service.EmpresaService.criar(empresa=request)
    if db_empresa is None:
        return JSONResponse(content={'detail': 'CNPJ deve ser único.'}, status_code=400)
    return JSONResponse(content={'detail': 'Criado com sucesso.', 'id': db_empresa.id, 'result':  EmpresaDTO.from_orm(db_empresa).model_dump()}, status_code=201)



@empresa.get("/")
def buscar_empresas(db: Session = Depends(get_db), id:int=None, cnpj:str=None, nome:str=None) -> JSONResponse:
    query = service.EmpresaService.buscar(id=id, cnpj=cnpj, nome=nome)

    response = [EmpresaDTO.from_orm(item).model_dump() for item in query]
    return JSONResponse(content={'detail': f'({len(query)}) item(s) foram encontrado(s).', 'result':response}, status_code=200)




@empresa.delete("/{id}")
def excluir_empresa_por_id(id:int, db: Session = Depends(get_db)) -> JSONResponse:
    if service.EmpresaService.excluir(id=id):
        return JSONResponse(content={'detail': 'Excluido com sucesso.'}, status_code=200)    
    return JSONResponse(content={'detail': f'Não foi possível localizar o id ({id}).'}, status_code=400)



@empresa.delete("/")
def excluir_empresa(request:EmpresaDTO, db: Session = Depends(get_db)) -> JSONResponse:
    if service.EmpresaService.excluir(cnpj=request.cnpj):
        return JSONResponse(content={'detail': 'Excluido com sucesso.'}, status_code=200)    
    return JSONResponse(content={'detail': f'Não foi possível localizar o cnpj ({request.cnpj}).'}, status_code=400)



@empresa.patch("/")
def editar_empresa(request:EmpresaDTO, db: Session = Depends(get_db)) -> JSONResponse:
    db_empresa = service.EmpresaService.editar(empresa=request)
    if db_empresa is None:
        return JSONResponse(content={'detail': f'Não foi possível localizar o cnpj ({request.cnpj}).'}, status_code=400)    
    return JSONResponse(content={'detail': 'Editado com sucesso.', 'content': EmpresaDTO.from_orm(db_empresa).model_dump() }, status_code=200)



@obrigacao_acessoria.post("/")
def criar_obrigacao_acessoria(request:ObrigacaoAcessoria_RequestDTO, db: Session = Depends(get_db)) -> JSONResponse:
    db_obrigacao_acessoria = service.ObrigacaoAcessoriaService.criar(obrigacaoAcessoria=request)    
    if db_obrigacao_acessoria is None:
        return JSONResponse(content={'detail': f'Não foi encontrada empresa de cnpj ({request.cnpj_empresa}).'}, status_code=400)    
    return JSONResponse(content={'detail': 'Criado com sucesso.', 'content': db_obrigacao_acessoria.model_dump()}, status_code=201)


@obrigacao_acessoria.delete("/")
def excluir_obrigacao_acessoria(request:ObrigacaoAcessoria_RequestDTO, db: Session = Depends(get_db)) -> JSONResponse:
    if service.ObrigacaoAcessoriaService.excluir(obrigacaoAcessoria=request):
        return JSONResponse(content={'detail': 'Excluido com sucesso.'}, status_code=200)
    return JSONResponse(content={'detail': f'Não foi encontrada obrigacao/acessoria de valores nome="{request.nome}" e empresa="{request.cnpj_empresa}").'}, status_code=400)

@obrigacao_acessoria.get("/")
def buscar_obrigacao_acessoria(db: Session = Depends(get_db), nome:str=None, periodicidade:str=None, cnpj_empresa:str=None ) -> str:
    db_obrigacao_acessoria = service.ObrigacaoAcessoriaService.buscar(nome=nome, periodicidade=periodicidade, cnpj_empresa=cnpj_empresa)
    print(db_obrigacao_acessoria)
    if len(db_obrigacao_acessoria) == 0:
        return JSONResponse(content={'detail': f'Não foram encontrada obrigacao/acessoria de valores nome="{nome}", empresa="{cnpj_empresa}") e periodicidade="{periodicidade}".'}, status_code=205)

    return JSONResponse(content={'detail': f'wasd', 'content':db_obrigacao_acessoria}, status_code=200)

