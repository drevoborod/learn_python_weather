# City temperature service
The service returns current city temperature.

To run, docker or Python 3.12 with fastapi and uvicorn required.

Requires the environment variable OPENWEATHER_APP_ID to be set.

Can be run using docker like this: `export OPENWEATHER_APP_ID="your_openweather_app_id" && docker-compose up`

The service will be accessible on the port 8881.