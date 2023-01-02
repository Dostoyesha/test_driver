import asyncio

from aiohttp import web

from api import get_channels_condition, post_channel_on, post_channel_off
from driver_utils import get_condition
from power_source_utils import PowerSupplyConnector


async def main():
    app = web.Application()

    app.router.add_get('/condition', get_channels_condition)
    app.router.add_post('/channel_on', post_channel_on)
    app.router.add_post('/channel_off', post_channel_off)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, 'localhost', 8000)
    await site.start()

    task = asyncio.create_task(get_condition())
    await task

    while True:
        await asyncio.sleep(3600)


if __name__ == '__main__':
    asyncio.run(main())
