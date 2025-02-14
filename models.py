from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
from database import Base
import schemas

class Empresa(Base):
    __tablename__ = "empresa_tb"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, index=True)
    cnpj = Column(String, unique=True)
    endereco = Column(String)
    telefone = Column(String)

    def __init__(self, dto:schemas.EmpresaDTO):
        self.nome = dto.nome
        self.cnpj = dto.cnpj
        self.endereco = dto.endereco
        self.telefone = dto.telefone


    def __repr__(self) -> str:
        return f"Empresa(id={self.id!r}, nome={self.nome!r}, cnpj={self.cnpj!r}, nome={self.nome!r}, endereco={self.endereco!r}, telefone={self.telefone!r})"


class ObrigacaoAcessoria(Base):
    __tablename__ = "obrigacaoAcessoria_tb"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String)
    periodicidade = Column(String)
    empresa = Column(Integer, ForeignKey(Empresa.id), index=True, nullable=False)

    def __repr__(self) -> str:
        return f"ObrigacaoAcessoria(id={self.id!r}, nome={self.nome}, periodicidade={self.periodicidade}, empresa={self.empresa})"
