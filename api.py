from aiohttp import web


async def get_channels_condition(request):
    print('Request GET')
    result = {'hello', 'word'}
    return web.Response(text=str(result))
    # return web.Response(text=json.dumps(result, ensure_ascii=False))


async def post_channel_on(request):
    print('Request POST')
    return web.Response(text='post channel on')


async def post_channel_off(request):
    print('Request POST')
    return web.Response(text='post channel off')

