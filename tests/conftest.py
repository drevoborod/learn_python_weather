import httpx
import pytest

from tests.data.weather_api_client import GET_EXISTING_CITY_RESPONSE_BODY, GET_NON_EXISTING_CITY_RESPONSE_BODY
from weather.clients import OpenweatherApiClient


def existing_city_handler(request):
    return httpx.Response(200, json=GET_EXISTING_CITY_RESPONSE_BODY)


def non_existing_city_handler(request):
    return httpx.Response(200, json=GET_NON_EXISTING_CITY_RESPONSE_BODY)


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def openweather_api_client_get_city_existing_city(anyio_backend) -> OpenweatherApiClient:
    url = "http://api.openweathermap.org"
    client = OpenweatherApiClient("abracadabra", url)
    client.client = httpx.AsyncClient(base_url=url, mounts={url: httpx.MockTransport(existing_city_handler)})
    return client


@pytest.fixture
async def openweather_api_client_get_city_non_existing_city(anyio_backend) -> OpenweatherApiClient:
    url = "http://api.openweathermap.org"
    client = OpenweatherApiClient("abracadabra", url)
    client.client = httpx.AsyncClient(base_url=url, mounts={url: httpx.MockTransport(non_existing_city_handler)})
    return client
