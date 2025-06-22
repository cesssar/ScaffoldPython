
# Scaffold Python com SQLAlchemy, Pydantic e SQL Server

Este repositório é um scaffold para um projeto Python utilizando SQLAlchemy para ORM, Pydantic para validações e configurações, e integração com SQL Server como banco de dados. Além disso, inclui configurações para testes automatizados e linting com `pytest` e `flake8`. Também há instruções para utilizar o `coverage` e o `SonarQube` (via Docker) para analisar a qualidade do código produzido.

A aplicação exemplo consulta uma API pública de CEP e salva os dados no banco de dados SQL Server.

## 📁 Estrutura do Projeto

```
scaffold/
├── app/
│   ├── __init__.py
│   ├── database.py           # Conexão com o banco de dados e modelo base
│   ├── interfaces/           # Interfaces para desacoplamento de classes
│   ├── models/               # Modelos de dados (ex: CEP)
│   ├── repositories/         # Lógica de persistência
│   ├── services/             # Lógica de negócios
│   └── utils/                # Métodos auxiliares
├── tests/                    # Testes unitários
│   ├── models/
│   ├── repositories/
│   └── services/
├── .env                      # Variáveis de ambiente
├── requirements.txt          # Dependências principais
├── requirements-dev.txt      # Dependências de desenvolvimento
├── main.py                   # Ponto de entrada
├── Makefile                  # Tarefas automatizadas
└── README.md                 # Este arquivo
```

## ✅ Requisitos

- Python 3.11
- SQL Server
- Dependências: `pyodbc`, `sqlalchemy`, `pytest`, `flake8`, `black`, etc.
- ODBC Driver 17 for SQL Server (ex: `sudo apt install msodbcsql17`)

## ⚙️ Instalação

```bash
# Clonar o repositório
git clone <url-do-repositorio>

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## 🔐 Configuração do .env

Crie o `.env` baseado no `env_example` com a string de conexão:

```
DATABASE_URL=mssql+pyodbc://usuario:senha@servidor:porta/banco?driver=ODBC+Driver+17+for+SQL+Server
```

## ▶️ Executando o Projeto

```bash
python main.py
```

## 🧪 Executando Testes

```bash
pytest
# ou
make test
```

## 🧹 Linting com flake8

```bash
flake8 app/ tests/
# ou
make lint
```

## 🎨 Formatação com black

```bash
black app/ tests/
# ou
make format
```

## 📊 Coverage (Cobertura de Testes)

```bash
coverage run -m pytest
coverage xml
```

## 📈 Análise com SonarQube (Local)

```bash
docker run -d --name sonarqube -p 9001:9000 sonarqube:latest
```

Acesse `http://localhost:9001`, configure o projeto, gere um token e instale o SonarScanner.

### Instalar SonarScanner

```bash
sudo apt-get install unzip
curl -sSLo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
unzip sonar-scanner.zip
sudo mv sonar-scanner-*/ /opt/sonar-scanner
export PATH=$PATH:/opt/sonar-scanner/bin
```

### Executar Análise

```bash
sonar-scanner -Dsonar.login=<seu_token>
```

Depois, acesse o painel web para visualizar o resultado.

![Painel SonarQube](https://github.com/cesssar/ScaffoldPython/blob/main/sonarqube.png)

## 📄 Licença

Este projeto está licenciado sob a MIT License.