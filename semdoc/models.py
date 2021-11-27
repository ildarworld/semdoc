from typing import Optional
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


@dataclass(frozen=True)
class WeatherResponseModel:
    base: str
    clouds: Optional[str]
    cod: str
    coord: dict
    dt: int
    id: int
    main: dict
    name: str
    sys: dict
    timezone: int
    visibility: int
    weather: list
    wind: dict

    @staticmethod
    def from_dict(dct: dict):
        return WeatherResponseModel(
            base=dct["base"],
            clouds=dct.get("clouds"),
            cod=dct["cod"],
            coord=dct["coord"],
            dt=dct["dt"],
            id=dct["id"],
            main=dct["main"],
            name=dct["name"],
            sys=dct["sys"],
            timezone=dct["timezone"],
            visibility=dct["visibility"],
            weather=dct["weather"],
            wind=dct["wind"],
        )
