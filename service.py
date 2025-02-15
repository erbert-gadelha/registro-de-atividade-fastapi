from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Empresa, ObrigacaoAcessoria
from schemas import EmpresaDTO, ObrigacaoAcessoria_RequestDTO, ObrigacaoAcessoria_ResponseDTO

db = next(get_db())

class __EmpresaService__():

    def __init__(self) -> None:
        pass
    
    def criar(self, empresa:EmpresaDTO) -> Empresa|None:
        db_empresa = Empresa(dto=empresa)
        try:
            db.add(db_empresa)
            db.commit()
            db.refresh(db_empresa)
        except Exception as e:
            db.rollback()
            return None
        return db_empresa
    
    def buscar(self, id:int=None, cnpj:str=None, nome:str=None) -> list[Empresa]:
        if(id!=None):
            return db.query(Empresa).filter_by(id=id).all()
        elif(cnpj!=None):
            return db.query(Empresa).filter_by(cnpj=cnpj).all()
        elif(nome!=None):
            return db.query(Empresa).filter_by(nome=nome).all()
        
        return db.query(Empresa).all()
    
    def excluir(self, id:int=None, cnpj:str=None) -> bool:
        db_empresa = None

        if id is not None:
            db_empresa = db.query(Empresa).filter_by(id=id).first()
        elif cnpj is not None:
            db_empresa = db.query(Empresa).filter_by(cnpj=cnpj).first()
        
        if db_empresa is None:
            return False
        
        try:
            db.delete(db_empresa)
            db.commit()
        except Exception as e:
            db.rollback()
            print(e)
            return False
        
        return True

    def editar(self, empresa:EmpresaDTO) -> Empresa|None:
        empresa_db = db.query(Empresa).filter_by(cnpj=empresa.cnpj).first()
        if empresa_db is None:
            return None
        
        try:
            empresa_db.nome = empresa.nome
            empresa_db.endereco = empresa.endereco
            empresa_db.telefone = empresa.telefone
            db.commit()
            db.refresh(empresa_db)
        except Exception as e:
            db.rollback()
            return None

        return empresa_db
    
class __ObrigacaoAcessoriaService__():

    def __init__(self) -> None:
        pass

    def criar(self, obrigacaoAcessoria:ObrigacaoAcessoria_RequestDTO,) -> ObrigacaoAcessoria_ResponseDTO|None:
        db_empresa = db.query(Empresa).filter_by(cnpj=obrigacaoAcessoria.cnpj_empresa).first()
        if db_empresa is None:
            return None
        
        obrigacao_acessoria = ObrigacaoAcessoria(empresa=db_empresa.id, nome=obrigacaoAcessoria.nome, periodicidade=obrigacaoAcessoria.periodicidade,)
        try:
            db.add(obrigacao_acessoria)
            db.commit()
            db.refresh(obrigacao_acessoria)
        except Exception as e:
            db.rollback()
            return None
        

        return ObrigacaoAcessoria_ResponseDTO(
            empresa=EmpresaDTO.from_orm(db_empresa).model_dump(),
            periodicidade=obrigacao_acessoria.periodicidade,
            nome=obrigacao_acessoria.nome
        )

    def buscar(self, nome:str=None, periodicidade:str=None, cnpj_empresa:str=None) -> list[ObrigacaoAcessoria_ResponseDTO]:
        query = []

        if cnpj_empresa is None and periodicidade is None and nome is None:
            query = db.query(ObrigacaoAcessoria).all()
        
        else:
            query = db.query(ObrigacaoAcessoria)

            if cnpj_empresa:
                db_empresa = EmpresaService.buscar(cnpj=cnpj_empresa)
                if len(db_empresa) == 1:
                    query = query.filter(ObrigacaoAcessoria.empresa == db_empresa[0].id)
            if periodicidade:
                query = query.filter(ObrigacaoAcessoria.periodicidade == periodicidade)
            if nome:
                query = query.filter(ObrigacaoAcessoria.nome.ilike(f"%{nome}%"))
            
            query = query.all()
        
        response = []
        for db_obrigacao_acessoria in query:
            db_empresa = EmpresaService.buscar(id=db_obrigacao_acessoria.empresa)
            if len(db_empresa) != 1:
                continue            
            response.append(
                ObrigacaoAcessoria_ResponseDTO(
                    nome=db_obrigacao_acessoria.nome,
                    periodicidade=db_obrigacao_acessoria.periodicidade,
                    empresa=EmpresaDTO.from_orm(db_empresa[0])                    
                    ).model_dump())
        return response
    
    def excluir(self, obrigacaoAcessoria:ObrigacaoAcessoria_RequestDTO) -> bool:
        db_empresa = db.query(Empresa).filter_by(cnpj=obrigacaoAcessoria.cnpj_empresa).first()
        if db_empresa is None:
            return False

        obrigacao_acessoria = db.query(ObrigacaoAcessoria).filter_by(nome=obrigacaoAcessoria.nome, empresa=db_empresa.id).first()
        if obrigacao_acessoria is None:
            return False
        
        try:
            db.delete(obrigacao_acessoria)
            db.commit()
        except Exception as e:
            db.rollback()
            return False
        
        return True
    




EmpresaService = __EmpresaService__()
ObrigacaoAcessoriaService = __ObrigacaoAcessoriaService__()

