import datetime as dt
import logging
import os
from functools import cache

import aiohttp
from aiohttp import web
from models import WeatherRequestParamsModel
from loader import WeatherClient

from repo import WeatherRepository
from db import session
from db import Weather

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


async def weather(request):
    """
    All params are required, datetime param is in YYYY-MM-DD HH:mm format only
    """
    status = 200
    params = WeatherRequestParamsModel(api=os.getenv("WEATHER_API"), **request.rel_url.query)
    log.info(f"\nRequest: {request=}, params: {request.rel_url.query}")

    exist = _get_weather_dict(**request.rel_url.query)
    if exist:
        log.info(f"Exists in db, returning from db")
        result = exist
    else:
        log.info(f"Not Exists in db, loading from weathermap")
        loader = WeatherClient(params)
        try:
            result = await loader.get()
            _add_weather(result, params.date)
        except aiohttp.ClientResponseError as ex:
            result, status = str(ex), 404
        except Exception as ex:
            result, status = str(ex), 500
    return web.Response(text=str(result), status=status)


@cache
def _get_weather_dict(city: str, country_code: str, date: str):
    repo = WeatherRepository()
    return repo.get(city=city, country_code=country_code, date=date)


def _add_weather(weather: dict, requested_dt: dt.datetime):
    w = Weather(**weather)
    w.requested_date = requested_dt
    repo = WeatherRepository()
    repo.add(w)


app = web.Application()
app.add_routes([web.get("/weather", weather)])

if __name__ == "__main__":
    log.info("Server started")
    web.run_app(app)
