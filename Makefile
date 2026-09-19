.PHONY: test-unit test-integration test-e2e test-all install run

PYTHON ?= .venv/bin/python
PYTEST ?= .venv/bin/pytest

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

run:
	.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

test-unit:
	$(PYTEST) -m unit -q

test-integration:
	$(PYTEST) -m integration -q

test-e2e:
	$(PYTEST) -m e2e -q

test-all:
	$(PYTEST) -q
