.PHONY: install run test-unit test-integration test-e2e test-all

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

run:
	.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Starter ships without a test suite — participants add tests in the labs.
test-unit test-integration test-e2e test-all:
	@echo "No test suite in this starter. Tests are built during the labs (Tag 1 Spec-Driven Lab 4; Tag 2 Test-Agent / run-tests)." >&2
	@exit 1
