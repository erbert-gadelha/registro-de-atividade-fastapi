from pydantic import BaseModel

class EmpresaDTO(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    telefone: str

    class Config:
        from_attributes = True

class ObrigacaoAcessoriaDTO(BaseModel):
    nome: str
    periodicidade: str
    empresa: EmpresaDTO

    class Config:
        from_attributes = True