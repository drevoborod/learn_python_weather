import pytest
from fastapi import HTTPException

from tests.data.weather_api_client import GET_EXISTING_CITY_RESPONSE_BODY


pytestmark = pytest.mark.anyio


class TestOpenweatherApiClient:
    async def test_get_city_by_name_successfull(self, openweather_api_client_get_city_existing_city):
        result = await openweather_api_client_get_city_existing_city.get_city_by_name("AnyCity")
        assert result.model_dump() == GET_EXISTING_CITY_RESPONSE_BODY[0]


    async def test_get_city_by_name_city_not_found(self, openweather_api_client_get_city_non_existing_city):
        with pytest.raises(HTTPException):
            await openweather_api_client_get_city_non_existing_city.get_city_by_name("AnyCity")
