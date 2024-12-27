run:
	uvicorn weather.main:app --host 0.0.0.0 --port 8881 --log-level debug

docker-run:
	docker build --build-arg OPENWEATHER_APP_ID=$${OPENWEATHER_APP_ID} -t weather .
	docker run --rm --network host weather
