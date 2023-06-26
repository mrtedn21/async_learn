import asyncio
import time
from concurrent.futures import ProcessPoolExecutor
from functools import partial


def count(count_to: int) -> int:
    start = time.time()
    counter = 0

    while counter < count_to:
        counter += 1

    end = time.time()
    print(f'finish count to {count_to} with time: {end - start}')
    return counter


async def main():
    with ProcessPoolExecutor() as process_pool:
        start_time = time.time()

        loop = asyncio.get_running_loop()
        nums = [1, 2000, 100000000, 200000000]
        calls = [partial(count, num) for num in nums]
        corutins = []

        for call in calls:
            corutins.append(loop.run_in_executor(process_pool, call))

        results = await asyncio.gather(*corutins)
        print(results)

        end_time = time.time()
        print(f'full time: {end_time - start_time}')


if __name__ == '__main__':
    asyncio.run(main())
