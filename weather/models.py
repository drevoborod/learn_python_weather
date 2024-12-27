from pydantic import BaseModel


class ErrorResponse(BaseModel):
    message: str


class GeoInfo(BaseModel):
    city_name: str
    city_country: str
    city_lat: float
    city_lon: float


class WeatherResponse(GeoInfo):
    current_temperature: float
    measurement_units: str
