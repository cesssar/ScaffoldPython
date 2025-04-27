# Scaffold Python com SQLAlchemy, Pydantic e SQL Server

Este repositório é um scaffold para um projeto Python utilizando SQLAlchemy para ORM, Pydantic para validações e configurações, e integração com SQL Server como banco de dados. Além disso, inclui configurações para testes automatizados e linting com pytest e flake8. Esta aplicação exemplo consulta uma API de CEP pública e salva os dados no banco de dados SQL Server.

## Estrutura do projeto

```
scaffold/
│
├── app/
│   ├── __init__.py
│   ├── database.py           # Conexão com o banco de dados e modelo base
│   ├── models/               # Modelos de dados (ex: CEP)
│   ├── repositories/         # Repositórios para lógica de persistência
│   ├── services/             # Lógica de negócios
│   ├── utils/                # Métodos auxiliares para utilizar em toda a aplicação
│   └── config.py             # Configurações do Pydantic
│
├── tests/                    # Testes unitários
│   ├── models/               # Testes para as implementações dentro de models
│   ├── repositories/         # Testes para as implementações dentro de repositories
│   └── services/             # Testes para as implementações dentro de services
│
├── .env                      # Variáveis de ambiente
├── requirements.txt          # Dependências principais do projeto
├── requirements-dev.txt      # Dependências para desenvolvimento (pytest, flake8, etc.)
├── main.py                   # Ponto de entrada do aplicativo
├── Makefile                  # Automação de tarefas (testes, linting, formatação)
└── README.md                 # Este arquivo
              

```

## Requisitos
 
- Python 3.11 (testado nesta versão)
- SQL Server como banco de dados
- Dependências: pyodbc, sqlalchemy, pytest, flake8, black, etc.

## Instalação

1) Clonar o repositório
2) Criar e ativar um ambiente virtual (recomendado):

```
python3.11 -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`

```

3) Instalar as dependẽncias do projeto

```
pip install -r requirements.txt

```

## Configuração arquivo .env

Crie um arquivo .env a partir do env_example na raiz do projeto e ajuste a seguinte variável de ambiente para configurar a URL de conexão com o SQL Server com as configurações do seu servidor:

```
DATABASE_URL=mssql+pyodbc://usuario:senha@servidor:porta/banco?driver=ODBC+Driver+17+for+SQL+Server

```

## Executando o projeto

O script main.py irá criar as tabelas no banco de dados se não existir, o mesmo irá solicitar um CEP para consulta na API e salvar o resultado no banco de dados.

```
python main.py

```

## Executando os testes unitários

Execute os testes com pytest ou com o comando do Makefile:

```
pytest

```

Ou 

```
make test

```

## Execute linting com flake8

Processo de análise de código-fonte para identificar se está de acordo com o guia de estilo da PEP8. Isso ajudará a garantir que o código esteja seguindo as boas práticas e tenha uma cobertura de testes adequada.


```
flake8 app/ tests/

```
Ou usando o makefile:

```
make lint

```

