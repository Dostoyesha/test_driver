import asyncio

from aiohttp import web

from api import get_channels_condition, post_channel_on, post_channel_off


def log_params(func):
    async def wrapper(*args, **kwargs):
        print("Time now is 0000")
        return await func(*args, **kwargs)
    return wrapper


@log_params
async def get_condition():
    while True:
        print("Condition from power supply is U, I, P")
        await asyncio.sleep(5)


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
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
