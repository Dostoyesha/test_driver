import asyncio

from aiohttp import web

from config import APP_API_HOST, APP_API_PORT, POWER_SUPPLY_CHANNELS_COUNT
from handlers import get_channels_condition, post_channel_on, post_channel_off
from utils import task_get_condition
from power_source import PowerSupplyConnector


async def app_run():
    app = web.Application()

    app.router.add_get('/condition', get_channels_condition)
    # app.router.add_post('/channel_on', post_channel_on)   # todo not completed
    app.router.add_post('/channel_off', post_channel_off)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, APP_API_HOST, APP_API_PORT)
    await site.start()

    ps_conn = PowerSupplyConnector(ch_count=POWER_SUPPLY_CHANNELS_COUNT)

    try:
        ps_conn.connect()
    except Exception as error:
        print('Connection to Power Supply failed.')
        return

    app.ps = ps_conn

    task = asyncio.create_task(task_get_condition(ps_conn))
    await task

    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt as e:
        print(e)
    finally:
        app.ps.disconnect()  # todo


if __name__ == '__main__':
    asyncio.run(app_run())
