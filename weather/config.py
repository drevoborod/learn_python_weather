import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    openweather_app_id: str
    openweather_base_url: str


def load_from_env() -> AppConfig:
    return AppConfig(
        openweather_app_id=os.environ["OPENWEATHER_APP_ID"],
        openweather_base_url="http://api.openweathermap.org",
    )
