from dataclasses import dataclass
from typing import Literal

from fastapi import HTTPException, status
import httpx
from httpx import HTTPStatusError, Response

from weather.models import City, Temperature, Error


@dataclass
class Coordinates:
    latitude: float
    longitude: float


class OpenweatherApiClient:
    def __init__(self, app_id: str, base_url: str) -> None:
        self.client = httpx.AsyncClient(base_url=base_url, params={"appid": app_id})

    async def get_city_by_name(self, city_name: str) -> City:
        response = await self.client.get(
            "/geo/1.0/direct",
            params={"q": city_name},
        )
        self._handle_openweather_api_error(response)
        response_body = response.json()
        if not response_body:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=Error(message=f"City '{city_name}' not found").model_dump())
        return City(
            name=response_body[0]["name"],
            country=response_body[0]["country"],
            lat=response_body[0]["lat"],
            lon=response_body[0]["lon"],
        )

    async def get_weather(
            self, coordinates: Coordinates, units: Literal["metric", "imperial"] = "metric"
    ) -> Temperature:
        response = await self.client.get(
            "/data/2.5/weather",
            params={"lat": coordinates.latitude, "lon": coordinates.longitude, "units": units},
        )
        self._handle_openweather_api_error(response)
        response_body = response.json()
        return Temperature(
            value=response_body["main"]["temp"],
            measurement_units="Celsius" if units == "metric" else "Fahrenheit"
        )

    def _handle_openweather_api_error(self, response: Response):
        try:
            response.raise_for_status()
        except HTTPStatusError as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Error(message=err.response.text).model_dump(),
            )

    async def close(self) -> None:
        await self.client.aclose()
