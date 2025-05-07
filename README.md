# Scaffold Python com SQLAlchemy, Pydantic e SQL Server

Este repositório é um scaffold para um projeto Python utilizando SQLAlchemy para ORM, Pydantic para validações e configurações, e integração com SQL Server como banco de dados. Além disso, inclui configurações para testes automatizados e linting com pytest e flake8. Também tem instruções de como utilizar o Coverabe e o SonarQube (via Docker) para analisar a qualidade do código produzido.
A aplicação utiliza método para log em arquivo já formatado para que seja lido pelo Elasticsearch.

Esta aplicação exemplo consulta uma API de CEP pública e salva os dados no banco de dados SQL Server.

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
│   └── utils/                # Métodos auxiliares para utilizar em toda a aplicação
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
- Driver ODBC Driver 17 for SQL Server para conexão com SQL Server em seu sistema operacional (exemplo Ubuntu instalar: sudo apt install msodbcsql17)

## Instalação

1) Clonar o repositório
2) Criar e ativar um ambiente virtual (recomendado):

```
python3.11 -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`

```

3) Instalar as dependências do projeto

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

## Executando linting com flake8

Processo de análise de código-fonte para identificar se está de acordo com o guia de estilo da PEP8. Isso ajudará a garantir que o código esteja seguindo as boas práticas e tenha uma cobertura de testes adequada.


```
flake8 app/ tests/

```

Ou usando o makefile:

```
make lint

```

## Executando formatação automática 

Este processo formata os códigos-fonte seguindo o guia de estilos da PEP8:

```
black app/ tests/

```

Ou usando o makefile:

```
make format

```

## Utilizando coverage (cobertura de testes)

Executar a análise e a geração do relatório em XML. Este relatório será exportado para o SonarQube nas próximas etapas para ser visualizado no painel web.

```
coverage run -m pytest
coverage xml


```


## Utilizando SonarQube para analisar o projeto localmente

- Instalar e subir o SonarQube via Docker com o comando abaixo ou com o docker-compose.yaml incluso no projeto:

```
docker run -d --name sonarqube -p 9001:9000 sonarqube:latest

```

Depois acessar http://localhost:9001 com usuário e senha admin (ele irá pedir para trocar a senha no primeiro acesso).

- Criar um Projeto no SonarQube:

Entra no painel SonarQube.
Clica em "Create Project".
Dá um nome para o seu projeto (ex: meu-projeto-python).
Vai gerar um Token de autenticação — guarda esse token, vamos usar depois. Ou ir em My Acount e gerar o token.

- Instalar o SonarScanner:

O SonarScanner é o agente que lê o seu código e manda os dados para o SonarQube.

Para Windows acessar https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/scanners/sonarscanner/

Instala via terminal (Ubuntu/Debian):

```
sudo apt-get install unzip
curl -sSLo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
unzip sonar-scanner.zip
sudo mv sonar-scanner-*/ /opt/sonar-scanner


```

Depois adiciona ao seu PATH:

```
export PATH=$PATH:/opt/sonar-scanner/bin

```

- Configurar o arquivo sonar-project.properties na raiz do projeto com o token gerado e o nome dado ao projeto no SonarQube.

- Rodar a análise via terminal (passando o token gerado no painel web)

```
sonar-scanner -Dsonar.login=sqp_ee0cf8f05674e0ed4f26fad2a5a544eb5d24439d

```

Ele vai:
- Analisar o código Python.
- Detectar bugs, code smells, vulnerabilidades.
- Subir o relatório para o SonarQube.


Acessar o painel web para visualizar o resultado.

![Painel SonarQube](https://github.com/cesssar/ScaffoldPython/blob/main/sonarqube.png)


## Licença

Este projeto está licenciado sob a MIT License.
