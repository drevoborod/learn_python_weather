from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from weather.clients import ApiClient
from weather.models import ErrorResponse, WeatherResponse


router = APIRouter()


@router.get(
    "/weather/",
    response_model=WeatherResponse,
    responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse}},
    summary="Get current temperature in specific city",
)
async def weather(request: Request, city: str, units: str = "metric"):
    async with ApiClient() as client:
        coords_model = await client.get_coordinates(city)
        if isinstance(coords_model, ErrorResponse):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=coords_model.model_dump())
        weather_data = await client.get_weather((coords_model.city_lat, coords_model.city_lon), units=units)
        if isinstance(weather_data, ErrorResponse):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=coords_model.model_dump())
        return WeatherResponse(
            current_temperature=weather_data[0],
            measurement_units=weather_data[1],
            city_name=coords_model.city_name,
            city_country=coords_model.city_country,
            city_lat=coords_model.city_lat,
            city_lon=coords_model.city_lon,
        )
