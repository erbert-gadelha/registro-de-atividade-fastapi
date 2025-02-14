from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
from database import Base

class Empresa(Base):
    __tablename__ = "empresa_tb"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cnpj = Column(String, unique=True)
    endereco = Column(String)
    telefone = Column(String)

    def __repr__(self) -> str:
        return f"Empresa(id={self.id!r}, nome={self.nome!r}, cnpj={self.cnpj!r}, nome={self.nome!r}, endereco={self.endereco!r}, telefone={self.telefone!r})"

