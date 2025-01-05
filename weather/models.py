from pydantic import BaseModel


class Error(BaseModel):
    message: str


class City(BaseModel):
    name: str
    country: str
    lat: float
    lon: float


class Temperature(BaseModel):
    value: float
    measurement_units: str


class Weather(BaseModel):
    temperature: Temperature
    city: City
