import datetime as dt
from functools import cache
import logging
import os

from aiohttp import web
from models import LocalWeatherRequestmodel
from loader import WeatherClient
from models import WeatherRequestParamsModel


log = logging.getLogger(__name__)


async def weather(request):
    params = LocalWeatherRequestmodel(**request.rel_url.query)

    params = WeatherRequestParamsModel(
        api=os.getenv("WEATHER_API"), country_code="RU", city="Moscow", date=dt.datetime.now
    )
    loader = WeatherClient(params)
    result = await loader.get()
    log.info(f"Request: {request=}, params: {request.rel_url.query}")
    return web.Response(text=str(result))


app = web.Application()
app.add_routes([web.get("/weather", weather)])

if __name__ == "__main__":
    web.run_app(app)
