import service
import models
import schemas
from database import Base, engine

def test_criar_empresa(db):
    service.db = db

    nome="SBT"
    cnpj="00.623.904/0001-71"
    telefone="4002-8922"
    endereco="Av. Boa Vista"  

    empresa = service.EmpresaService.criar(
        schemas.EmpresaDTO(
            nome=nome,
            cnpj=cnpj,
            telefone=telefone,
            endereco=endereco
        ))

    assert empresa is not None
    assert isinstance(empresa, models.Empresa)
    assert empresa.nome == nome
    assert empresa.cnpj == cnpj
    assert empresa.telefone == telefone
    assert empresa.endereco == endereco

def test_buscar_empresa(db):
    service.db = db

    cnpj="00.623.904/0001-71"
    telefone="4002-8922"
    endereco="Av. Boa Vista" 

    service.EmpresaService.criar(schemas.EmpresaDTO(nome=   "SBT", cnpj=cnpj, telefone=telefone, endereco=endereco))
    service.EmpresaService.criar(schemas.EmpresaDTO(nome= "Globo", cnpj=cnpj, telefone=telefone, endereco=endereco))
    service.EmpresaService.criar(schemas.EmpresaDTO(nome="Record", cnpj=cnpj, telefone=telefone, endereco=endereco))

    empresas = service.EmpresaService.buscar(nome='SBT')
    assert empresas is not None
    assert len(empresas) == 1
    assert empresas[0].nome == 'SBT'

def test_editar_empresa(db):
    service.db = db

    nome="SBT"
    cnpj="00.623.904/0001-71"
    telefone="4002-8922"
    endereco="Av. Boa Vista"  

    empresa = service.EmpresaService.criar(
        schemas.EmpresaDTO(
            nome="nome",
            cnpj=cnpj,
            telefone="telefone",
            endereco="endereco"
        ))
    
    empresa = service.EmpresaService.editar(
        schemas.EmpresaDTO(
            nome=nome,
            cnpj=cnpj,
            telefone=telefone,
            endereco=endereco
        ))

    assert empresa is not None
    assert isinstance(empresa, models.Empresa)
    assert empresa.nome == nome
    assert empresa.cnpj == cnpj
    assert empresa.telefone == telefone
    assert empresa.endereco == endereco



def test_excluir_empresa(db):
    service.db = db

    cnpj = "00.623.904/0001-71"

    service.EmpresaService.criar(
        schemas.EmpresaDTO(
            nome="SBT",
            cnpj=cnpj,
            telefone="4002-8922",
            endereco="Av. Boa Vista"
        ))
    
    service.EmpresaService.excluir(cnpj=cnpj)
    empresas = service.EmpresaService.buscar()

    assert empresas is not None
    assert all(empresa.cnpj != cnpj for empresa in empresas)
