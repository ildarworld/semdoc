import abc
import datetime as dt
from datetime import timezone
import logging
from typing import Any
from db import session
from db import Weather


log = logging.getLogger(__name__)


class AbstractRepository(abc.ABC):
    """Vase repo for service"""

    @abc.abstractmethod  # (1)
    def add(self, *args, **kwargs):
        raise NotImplementedError  # (2)

    @abc.abstractmethod
    def get(self, reference) -> Any:
        raise NotImplementedError


class WeatherRepository(AbstractRepository):
    """Weather repo"""

    def add(self, weather: Weather):
        with session() as s:
            s.add(weather)

    def get(self, country_code: str, city: str, date: str):
        # TODO use country code if it is required
        # TODO handle city names as with ' at the end, e.g. Kazan and Kazan'
        log.info(f"Get data from db {city} {date}")
        with session() as s:
            weather = (
                s.query(Weather)
                .filter_by(name=city, requested_date=dt.datetime.strptime(date, "%Y-%m-%d %H:%M"))
                .first()
            )
            if weather:
                return weather.as_dict()
