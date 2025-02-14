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
