import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Cria um banco de dados em memória para os testes
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
SessionTesting = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db():
    # Cria as tabelas antes de cada teste
    Base.metadata.create_all(bind=engine)
    session = SessionTesting()

    yield session  # Retorna a sessão para o teste usar

    # Limpa o banco de dados após o teste
    session.close()
    Base.metadata.drop_all(bind=engine)
