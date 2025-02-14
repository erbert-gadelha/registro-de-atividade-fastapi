from fastapi import APIRouter, Depends
import psycopg2
from sqlalchemy.orm import Session
from database import get_db
from models import Empresa
from starlette.responses import JSONResponse
from schemas import EmpresaDTO


empresa = APIRouter(prefix="/empresa")

@empresa.post("/")
def criar_empresa(request:EmpresaDTO, db: Session = Depends(get_db)) -> JSONResponse:
    db_empresa = Empresa(dto=request)

    try:
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
    except Exception as e:
        return JSONResponse(content={
            'detail': 'CNPJ deve ser único.'
        }, status_code=400)

    dto = EmpresaDTO.from_orm(db_empresa).model_dump()
    return JSONResponse(content={
        'detail': 'Criado com sucesso.',
        'id': db_empresa.id,
        'result': dto
    }, status_code=201)

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
    return JSONResponse(content={
        'detail': f'({len(query)}) item(s) foram encontrado(s).',
        'result':query
    }, status_code=200)
