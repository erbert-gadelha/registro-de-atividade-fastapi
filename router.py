from fastapi import APIRouter, Depends
import psycopg2
from sqlalchemy.orm import Session
from database import get_db
from models import Empresa, ObrigacaoAcessoria
from starlette.responses import JSONResponse
from schemas import EmpresaDTO, ObrigacaoAcessoria_RequestDTO, ObrigacaoAcessoria_ResponseDTO


empresa = APIRouter(prefix="/empresa")
obrigacao_acessoria = APIRouter(prefix="/obrigacao-acessoria")

@empresa.post("/")
def criar_empresa(request:EmpresaDTO, db: Session = Depends(get_db)) -> JSONResponse:
    db_empresa = Empresa(dto=request)
    try:
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
    except Exception as e:
        db.rollback()
        return JSONResponse(content={'detail': 'CNPJ deve ser único.'}, status_code=400)

    dto = EmpresaDTO.from_orm(db_empresa).model_dump()
    return JSONResponse(content={'detail': 'Criado com sucesso.', 'id': db_empresa.id, 'result': dto}, status_code=201)

@empresa.get("")
def pegar_empresas(db: Session = Depends(get_db), id:int=None, cnpj:str=None, nome:str=None) -> JSONResponse:
    query=[]
    if(id!=None):
        query = db.query(Empresa).filter_by(id=id).all()
    elif(cnpj!=None):
        query = db.query(Empresa).filter_by(cnpj=cnpj).all()
    elif(nome!=None):
        query = db.query(Empresa).filter_by(nome=nome).all()     

    query = [EmpresaDTO.from_orm(item).model_dump() for item in query]
    return JSONResponse(content={'detail': f'({len(query)}) item(s) foram encontrado(s).', 'result':query}, status_code=200)


@empresa.delete("/{id}")
def excluir_empresa_por_id(id:int, db: Session = Depends(get_db)) -> JSONResponse:
    empresa = db.query(Empresa).filter_by(id=id).first()
    if empresa is None:
        return JSONResponse(content={'detail': f'Não foi possível localizar o id ({id}).'}, status_code=400)
    try:
        db.delete(empresa)
        db.commit()
    except Exception as e:
        db.rollback()
        return JSONResponse(content={'detail': 'Erro do sistema.'}, status_code=400)
    return JSONResponse(content={'detail': 'Excluido com sucesso.'}, status_code=200)


@empresa.delete("/")
def excluir_empresa(request:EmpresaDTO, db: Session = Depends(get_db)) -> JSONResponse:
    empresa = db.query(Empresa).filter_by(cnpj=request.cnpj).first()
    if empresa is None:
        return JSONResponse(content={'detail': f'Não foi possível localizar o cnpj ({request.cnpj}).'}, status_code=400)
    try:
        db.delete(empresa)
        db.commit()
    except Exception as e:
        db.rollback()
        return JSONResponse(content={'detail': 'Erro do sistema.'}, status_code=400)
    return JSONResponse(content={'detail': 'Excluido com sucesso.'}, status_code=200)

@empresa.patch("/")
def editar_empresa(request:EmpresaDTO, db: Session = Depends(get_db)) -> JSONResponse:
    empresa = db.query(Empresa).filter_by(cnpj=request.cnpj).first()
    if empresa is None:
        return JSONResponse(content={'detail': f'Não foi possível localizar o cnpj ({request.cnpj}).'}, status_code=400)    
    try:
        empresa.nome = request.nome
        empresa.endereco = request.endereco
        empresa.telefone = request.telefone
        db.commit()
        db.refresh(empresa)
    except Exception as e:
        db.rollback()
        return JSONResponse(content={'detail': 'Erro do sistema.'}, status_code=400)

    return JSONResponse(content={'detail': 'Editado com sucesso.', 'content': EmpresaDTO.from_orm(empresa).model_dump() }, status_code=200)




@obrigacao_acessoria.post("/")
def criar_obrigacao_acessoria(request:ObrigacaoAcessoria_RequestDTO, db: Session = Depends(get_db)) -> JSONResponse:
    empresa = db.query(Empresa).filter_by(cnpj=request.cnpj_empresa).first()
    if empresa is None:
            return JSONResponse(content={'detail': f'Não foi encontrada empresa de cnpj ({request.cnpj_empresa}).'}, status_code=400)

    obrigacao_acessoria = ObrigacaoAcessoria()
    obrigacao_acessoria.empresa = empresa.id
    obrigacao_acessoria.nome = request.nome
    obrigacao_acessoria.periodicidade = request.periodicidade

    try:
        db.add(obrigacao_acessoria)
        db.commit()
        db.refresh(obrigacao_acessoria)
    except Exception as e:
        db.rollback()
        print ("e", e.__class__)
        return JSONResponse(content={'detail': 'Erro do sistema.'}, status_code=400)
    
    responseDTO = ObrigacaoAcessoria_ResponseDTO(
        empresa=empresa,
        periodicidade=obrigacao_acessoria.periodicidade,
        nome=obrigacao_acessoria.nome
    ).model_dump()
    
    return JSONResponse(content={'detail': 'Cirado com sucesso.', 'content': responseDTO}, status_code=201)
