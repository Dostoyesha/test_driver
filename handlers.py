import json

from aiohttp import web

from utils import prepare_condition_data

routes = web.RouteTableDef()


@routes.get('/condition')
async def get_channels_condition(request):
    conn = request.app.ps
    ch_count = conn.ch_count

    ch_measures_map = {ch: await conn.get_ch_measures(ch) for ch in range(ch_count + 1)}
    json_data = prepare_condition_data(ch_measures_map)

    return web.Response(text=json.dumps(json_data), status=200)


@routes.post('/channel_on')
async def post_channel_on(request):
    conn = request.app.ps

    ch = request.query.get('ch')
    current = request.query.get('current')  # todo json
    voltage = request.query.get('voltage')  # todo json

    if ch and current and voltage:
        ch, current, voltage = int(ch), float(current), float(voltage)
        try:
            conn.set_current(ch, current)
            conn.set_voltage(ch, voltage)
            conn.turn_on_ch_output(ch)

            code, response = 200, {'massage': f'Channel {ch} turned ON with measures: U {voltage}, I {current}.'}

        except Exception as error:
            code, response = 502, {'massage': f'Error by executing ON commands on PS for channel {ch}.',
                                   'error': str(error)}
    else:
        code, response = 400, {'massage': f'Must be specified all params: ch, current and voltage.'}

    return web.Response(text=json.dumps(response), status=code)


@routes.post('/channel_off')
async def post_channel_off(request):
    conn = request.app.ps
    ch = request.query.get('ch')

    if ch:
        ch = int(ch)
        try:
            conn.turn_off_ch_output(ch)
            code, response = 200, {'massage': f'Channel {ch} turned OFF.'}

        except Exception as error:
            code, response = 502, {'massage': f'Error by executing OFF command on PS for channel {ch}.',
                                   'error': str(error)}
    else:
        code, response = 400, {'massage': 'Must be specified ch param.'}

    return web.Response(text=json.dumps(response), status=code)

