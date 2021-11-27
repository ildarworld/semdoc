import datetime as dt
from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherRequestParamsModel:
    country_code: str
    city: str
    api: str
    date: dt.date

    def dict(self):
        return dict(country_code=self.country_code, city=self.city, date=self.date, api=self.api)
