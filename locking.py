import asyncio
from asyncio import Lock


async def a(lock: Lock):
    print('corutine waiting to get lock')
    async with lock:
        print('corutine in critic section')
        await asyncio.sleep(2)
    print('corutine free the lock')


async def b(lock: Lock):
    print('second corutine waiting to get lock')
    async with lock:
        print('second corutine in critic section')
        await asyncio.sleep(2)
    print('second corutine free the lock')


async def main():
    lock = Lock()
    await asyncio.gather(a(lock), b(lock))


asyncio.run(main())

