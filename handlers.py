import json

from aiohttp import web

from utils import prepare_condition_data


async def get_channels_condition(request):
    conn = request.app.ps
    ch_count = conn.ch_count

    try:
        ch_measures_map = {ch: await conn.get_ch_measures(ch) for ch in range(1, ch_count + 1)}
        data = prepare_condition_data(ch_measures_map)
    except Exception as error:
        return web.Response(text=json.dumps({'message': 'Error by PS measures getting.', 'error': str(error)}),
                            status=502)

    return web.Response(text=json.dumps(data), status=200)


async def post_channel_on(request):
    """todo complete"""

    conn = request.app.ps

    ch = request.query.get('ch')
    current = request.query.get('current')  # todo to json
    voltage = request.query.get('voltage')  # todo to json

    if ch and current and voltage:
        ch, current, voltage = int(ch), float(current), float(voltage)
        try:
            await conn.set_current(ch, current)
            await conn.set_voltage(ch, voltage)
            await conn.turn_on_ch_output(ch)

            code, response = 200, {'message': f'Channel {ch} turned ON with measures: U {voltage}, I {current}.'}

        except Exception as error:
            code, response = 502, {'message': f'Error by executing ON commands on PS for channel {ch}.',
                                   'error': str(error)}
    else:
        code, response = 400, {'message': f'Must be specified all params: ch, current and voltage.'}

    return web.Response(text=json.dumps(response), status=code)


async def post_channel_off(request):
    conn = request.app.ps
    ch = request.query.get('ch')

    if not ch:
        return web.Response(status=400, text=json.dumps({'message': 'Must be specified ch param.'}))

    ch = int(ch)
    try:
        await conn.turn_off_ch_output(ch)
    except Exception as error:
        data = {'message': f'Error by executing OFF command on PS for channel {ch}.', 'error': str(error)}
        return web.Response(status=502, text=json.dumps(data))

    return web.Response(text=json.dumps({'message': f'Channel {ch} turned OFF.'}), status=200)

