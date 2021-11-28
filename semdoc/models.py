from typing import Optional
import datetime as dt
from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherRequestParamsModel:
    country_code: str
    city: str
    api: str
    date: dt.datetime
