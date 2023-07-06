import asyncio
import functools
from asyncio import Event


def trigger_event(event: Event):
    print('Activating event')
    event.set()


async def do_work_on_event(event: Event):
    print('Wait for event')
    await event.wait()
    print('Working!!!!')
    await asyncio.sleep(1)
    print('Work finish')
    event.clear()


async def main():
    event = asyncio.Event()
    asyncio.get_running_loop().call_later(
        5, functools.partial(trigger_event, event)
    )
    await asyncio.gather(
        do_work_on_event(event), do_work_on_event(event),
    )


asyncio.run(main())

