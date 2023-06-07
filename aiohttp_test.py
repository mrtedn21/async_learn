import asyncio
import aiohttp
from aiohttp import ClientSession
from datetime import datetime


async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status


async def main():
    async with aiohttp.ClientSession() as session:
        d1 = datetime.now()
        url = 'https://crontab.guru/'

        tasks = [asyncio.create_task(fetch_status(session, url)) for i in range(1000)]
        [await task for task in tasks]

        await asyncio.gather(*[fetch_status(session, url) for _ in range(1000)])
        d2 = datetime.now()
        print(d2-d1)


if __name__ == '__main__':
    asyncio.run(main())
