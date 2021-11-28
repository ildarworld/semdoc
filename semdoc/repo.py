import abc
import datetime as dt
from datetime import timezone
import logging
from typing import Any
from db import session
from db import Weather


log = logging.getLogger(__name__)


def str_to_unix_timestamp(value: str) -> int:
    d = dt.datetime.strptime(value, "%Y-%m-%d %H:%M")
    return int(d.strftime("%s"))


def clean_time_stamp_dt(ts: int) -> int:
    d = dt.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    return str_to_unix_timestamp(d)


class AbstractRepository(abc.ABC):
    @abc.abstractmethod  # (1)
    def add(self, *args, **kwargs):
        raise NotImplementedError  # (2)

    @abc.abstractmethod
    def get(self, reference) -> Any:
        raise NotImplementedError


class WeatherRepository(AbstractRepository):
    def add(self, weather: Weather):
        weather.dt = clean_time_stamp_dt(weather.dt)
        with session() as s:
            s.add(weather)

    def get(self, country_code: str, city: str, date: str):
        log.info(f"Get data from db {city} {date}")
        with session() as s:
            weather = (
                s.query(Weather)
                .filter_by(name=city, requested_date=dt.datetime.strptime(date, "%Y-%m-%d %H:%M"))
                .first()
            )
            if weather:
                return weather.as_dict()
