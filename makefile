.PHONY: test lint format

# Roda os testes unitários
test:
	pytest -q --disable-warnings tests/

# Checa o código com flake8 quanto a aderência a PEP8 (lint)
lint:
	flake8 app/ tests/

# Formata o código com black
format:
	black app/ tests/

# Roda tudo (lint + test)
check: lint test