.PHONY: test lint run docker-build all

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/

run:
	uvicorn code_eval_sandbox.main:app --host 0.0.0.0 --port 8080 --reload

docker-build:
	docker build -t agentic-code-eval-sandbox .

all: lint test
