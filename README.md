# Registro de Atividades com fastapi
Essa plicação se trata de um `CRUD` simples desenvolvido em python com frameworks como **FastAPI**, **Pydantic** e **SQLAlchemy**.
As rotas são documentadas por meio do **Swagger UI** e podem ser acessadas através de {endereco-base}/docs `(ex. localhost:8080/docs)`.
A aplicação possui apenas duas rotas: `/empresa` e `/obrigacao-acessoria` que respondem aos métodos `GET`, `POST`, `DELETE` e `PATCH` do HTTP.

## Definindo o ambiente de execução
    python3 -m venv venv
    source venv/bin/activate
 atribua as variáveis de ambiente com as credencias do seu bando de dados

    #credencias definidas para docker anexo a aplicacao
    DB_HOST=localhost
    DB_PORT=:5432
    DB_NAME=meubanco
    DB_USER=user
    DB_PW=

## Instalando dependencias
    pip install -r requirements.txt
## Executando a Aplicacao

    uvicorn main:app

O banco postgree pode ser executado através de

    docker-compose up -d

 
## Execução dos Testes

    pytest # na pasta raiz da aplicação

