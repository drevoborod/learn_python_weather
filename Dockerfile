FROM python:3.12-slim

RUN apt-get update; apt-get install -y --no-install-recommends make; \
	rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY weather /app/weather
COPY Makefile /app/

ENTRYPOINT []
# CMD ["uvicorn", "weather.main:app", "--host", "0.0.0.0", "--port", "8881", "--log-level", "debug"]
CMD ["make", "run"]