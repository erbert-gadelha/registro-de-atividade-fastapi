import service
import models
import schemas
from database import Base, engine

def test_criar_obrigacao_acessoria(db):
    service.db = db

    cnpj="00.623.904/0001-71"
    service.EmpresaService.criar(schemas.EmpresaDTO(nome="SBT", cnpj=cnpj, telefone="4002-8922", endereco="Av. Boa Vista"))

    obrigacao_acessoria = service.ObrigacaoAcessoriaService.criar(
        schemas.ObrigacaoAcessoria_RequestDTO(
            nome="emitir pagamentos",
            periodicidade="diariamente",
            cnpj_empresa=cnpj
        ))

    assert obrigacao_acessoria is not None
    assert isinstance(obrigacao_acessoria, schemas.ObrigacaoAcessoria_ResponseDTO)
    assert obrigacao_acessoria.empresa is not None
    assert obrigacao_acessoria.empresa.cnpj == cnpj

def test_excluir_obrigacao_acessoria(db):
    service.db = db

    nome="emitir pagamentos"
    periodicidade="diariamente"
    cnpj_empresa="00.623.904/0001-71"

    service.EmpresaService.criar(schemas.EmpresaDTO(nome="SBT", cnpj=cnpj_empresa, telefone="4002-8922", endereco="Av. Boa Vista"))
    service.ObrigacaoAcessoriaService.criar(schemas.ObrigacaoAcessoria_RequestDTO(nome=nome, periodicidade=periodicidade, cnpj_empresa=cnpj_empresa))

    foi_excluido = service.ObrigacaoAcessoriaService.excluir(schemas.ObrigacaoAcessoria_RequestDTO(nome=nome, periodicidade=periodicidade, cnpj_empresa=cnpj_empresa))

    busca = service.ObrigacaoAcessoriaService.buscar()

    assert foi_excluido is True
    assert all(obrigacao.nome != nome and obrigacao.periodicidade != periodicidade and obrigacao.empresa.cnpj != cnpj_empresa  for obrigacao in busca)