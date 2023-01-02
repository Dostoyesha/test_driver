from aiohttp import web

from driver_utils import PSCommandsHandler
from power_source_utils import PowerSupplyConnector


async def get_channels_condition(request):

    ps = PowerSupplyConnector()
    await ps.connect()

    handler = PSCommandsHandler(ps)
    conditions_data = handler.get_conditions()

    await ps.disconnect()

    return web.Response(text=str(conditions_data))
    # return web.Response(text=json.dumps(result, ensure_ascii=False))


async def post_channel_on(request):
    print('Request POST')
    return web.Response(text='post channel on')


async def post_channel_off(request):
    print('Request POST')
    return web.Response(text='post channel off')

