import asyncio

from aiohttp import web

from utils import task_get_condition
from handlers import routes
from power_source import PowerSupplyConnector


async def main():
    app = web.Application()

    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, 'localhost', 8000)   # todo config?
    await site.start()

    ps_conn = PowerSupplyConnector()

    try:
        await ps_conn.connect() # todo можно ли коннект делать асинхронным?
    except Exception as error:
        print('Connection to Power Supply failed.')
        return

    app.ps = ps_conn

    task = asyncio.create_task(task_get_condition(ps_conn))
    await task

    while True:
        await asyncio.sleep(3600)

    # await ps.disconnect() # todo


if __name__ == '__main__':
    asyncio.run(main())
