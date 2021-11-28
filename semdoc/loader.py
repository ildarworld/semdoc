import asyncio
import datetime as dt
import logging
from functools import partialmethod
import os

import aiohttp

from models import WeatherRequestParamsModel


log = logging.getLogger(__name__)


class WeatherClient:
    """Загрузка информации о погоде"""

    URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, req_params: WeatherRequestParamsModel, session: aiohttp.ClientSession = None):
        self.req_params = req_params
        if session is None:
            session = aiohttp.ClientSession(raise_for_status=True)
        self.session = session

    @property
    def params(self):
        return {
            "q": "{city},{country}".format(city=self.req_params.city, country=self.req_params.country_code),
            "appid": self.req_params.api,
        }

    async def _request(self):
        # TODO handle exceptions
        async with self.session.get(self.URL, params=self.params) as response:
            log.info(f"STATUS:{response.status} | PARAMS: {self.params} | RESPONSE: {response.text}")
            return await response.json()

    async def _get(self):
        response = await self._request()
        return response

    get = partialmethod(_get)

    async def close(self):
        await self.session.close()


if __name__ == "__main__":

    async def load():
        params = WeatherRequestParamsModel(
            api=os.getenv("WEATHER_API"), country_code="RU", city="Moscow", date=dt.datetime.now
        )
        loader = WeatherClient(params)
        result = await loader.get()
        await loader.close()
        from pprint import pprint

        pprint(result)

    asyncio.run(load())
