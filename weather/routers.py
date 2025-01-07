from typing import Annotated, Literal

from fastapi import APIRouter, status, Depends

from weather.clients import OpenweatherApiClient, Coordinates
from weather.config import load_from_env
from weather.models import Error, Weather


router = APIRouter()


async def openweather_client() -> OpenweatherApiClient:
    config = load_from_env()
    client = OpenweatherApiClient(app_id=config.openweather_app_id, base_url=config.openweather_base_url)
    try:
        yield client
    finally:
        await client.close()


@router.get(
    "/weather/",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": Error},
        status.HTTP_404_NOT_FOUND: {"model": Error},
    },
    summary="Get current temperature in specific city",
)
async def weather(
        client: Annotated[Weather, Depends(openweather_client)],
        city: str,
        units: Literal["metric", "imperial"] = "metric"
) -> Weather:
    city_info = await client.get_city_by_name(city)
    temperature = await client.get_weather(Coordinates(longitude=city_info.lon, latitude=city_info.lat), units=units)
    return Weather(
        city=city_info,
        temperature=temperature,
    )
