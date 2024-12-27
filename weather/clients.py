import asyncio
import os
from http import HTTPStatus
from typing import Literal

import aiohttp

from weather.models import GeoInfo, ErrorResponse


type Coordinates = tuple[float, float]
type Temperature = tuple[float, str]


class ApiClient:
    def __init__(self):
        self.app_id = os.getenv("OPENWEATHER_APP_ID")
        if not self.app_id:
            raise ValueError("OPENWEATHER_APP_ID environment variable should be set before running the service")

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def _get(self, url: str, params: dict) -> dict | list | ErrorResponse:
        params["appid"] = self.app_id
        async with self.session.get(url=url, params=params) as response:
            if response.status != HTTPStatus.OK:
                return ErrorResponse(message=f"Request to {url} had status {response.status}.\n"
                                             f"Raw contents: {await response.text()}")
            return await response.json()

    async def get_coordinates(self, city_name: str) -> GeoInfo | ErrorResponse:
        response = await self._get(
            "http://api.openweathermap.org/geo/1.0/direct",
            {"q": city_name},
        )
        if isinstance(response, ErrorResponse):
            return response
        if not response:
            return ErrorResponse(message=f"City '{city_name}' has not been found")

        data = GeoInfo(
            city_name=response[0]["name"],
            city_country=response[0]["country"],
            city_lat=response[0]["lat"],
            city_lon=response[0]["lon"],
        )
        return data


    async def get_weather(
            self, coordinates: Coordinates, units: Literal["metric", "imperial"] = "metric"
    ) -> Temperature | ErrorResponse:
        response = await self._get(
            "https://api.openweathermap.org/data/2.5/weather",
            {"lat": coordinates[0], "lon": coordinates[1], "units": units},
        )
        if isinstance(response, ErrorResponse):
            return response
        return response["main"]["temp"], "Celsius" if units == "metric" else "Fahrenheit"


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
