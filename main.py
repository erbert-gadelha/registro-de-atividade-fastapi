from fastapi import FastAPI

from fastapi import FastAPI
from database import Base, engine
import router

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router.empresa, tags=["Empresas"])
app.include_router(router.obrigacao_acessoria, tags=["Obrigacao e Acessoria"])
