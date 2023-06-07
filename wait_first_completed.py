import asyncio
import aiohttp


async def fetch_status(session, url):
    response = await session.get(url)
    return response.status


async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://crontab.guru/'
        pending = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
        ]

        while pending:
            done, pending = await asyncio.wait(
                pending,
                return_when=asyncio.FIRST_COMPLETED,
            )

            for done_task in done:
                if done_task.exception() is None:
                    print(done_task.result())


if __name__ == '__main__':
    asyncio.run(main())
