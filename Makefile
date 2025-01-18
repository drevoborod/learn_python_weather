lint:
	mypy weather

test:
	pytest tests

run:
	uvicorn weather.main:app --host 0.0.0.0 --port 8881 --log-level debug
