FROM python:3.12-slim

WORKDIR /usr/src/weather

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ARG OPENWEATHER_APP_ID
ENV OPENWEATHER_APP_ID=$OPENWEATHER_APP_ID

ENTRYPOINT [ "uvicorn", "weather.main:app", "--host", "0.0.0.0", "--port", "8881", "--log-level", "debug" ]