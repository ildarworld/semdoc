import asyncio
import datetime as dt
import logging
from functools import partialmethod
import os

import aiohttp

log = logging.getLogger(__name__)


class WeatherClient:
    """Загрузка информации о погоде"""

    URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(
        self, api_key: str, country_code: str, city: str, date: dt.date, session: aiohttp.ClientSession = None
    ):
        self.api_key = api_key
        self.country_code = country_code
        self.city = city
        self.date = date
        if session is None:
            session = aiohttp.ClientSession(raise_for_status=True)
        self.session = session

    @property
    def params(self):
        return {"q": "{city},{country}".format(city=self.city, country=self.country_code), "appid": self.api_key}

    async def _request(self):
        async with self.session.get(self.URL, params=self.params) as response:
            log.info(f"STATUS:{response.status} | PARAMS: {self.params} | RESPONSE: {response.text}")
            return await response.json()

    get = partialmethod(_request)

    async def close(self):
        await self.session.close()


if __name__ == "__main__":

    async def load():
        loader = WeatherClient(api_key=os.getenv("WEATHER_API"), country_code="RU", city="Moscow", date=dt.datetime.now)
        result = await loader.get()
        await loader.close()
        from pprint import pprint

        pprint(result)

    asyncio.run(load())
