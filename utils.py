import asyncio


def parse_ch_measures(raw_data):
    """
    Not completed.

    :param raw_data: ':SOMEdata:current:voltage:power'
    :return:
        {'current': '1.0001',
        'voltage': '2.0002',
        'power': '3'}
    """
    result = {
        'current': None,
        'voltage': None,
        'power': None
    }
    # todo
    return {'current': '1.0001',
            'voltage': '2.0002',
            'power': '3'}


def prepare_ch_measures_data(ch, raw_data):
    """
    Not completed.

    :param ch: number of channel
    :param raw_data: data from ps 'some U I P' to parsing

    :return: dict of channel params
        {'channel': '1',
        'current': '1.0001',
        'voltage': '2.0002',
        'power': '3'}
    """
    # todo
    result = {'channel': ch}

    measures = parse_ch_measures(raw_data)
    result.update(measures)

    return result


def prepare_condition_data(ch_measures_map):
    """
    :param ch_measures_map: dict with key - channel number, value - measures data from ps
        {1: 'measures data',
        2: 'measures data'}

    :returns list of dicts with measures of channel
        [{'channel': '1',
        'current': '1.0001',
        'voltage': '2.0002',
        'power': '3'},
        {'channel': '2',
        'current': '3.0001',
        'voltage': '4.0002',
        'power': '5'},
        ..
        ]
    """
    return [prepare_ch_measures_data(ch, data) for ch, data in ch_measures_map]


def log_ch_measures(func):
    """
    Not comleted.

    :param func:
    :return:
    """
    async def wrapper(*args, **kwargs):
        raw_data = await func(*args, **kwargs)
        data = parse_ch_measures(raw_data)
        print(data)  # todo to file
    return wrapper


async def task_get_condition(ps_conn):
    """
    Not completed.

    :param ps_conn:
    :return:
    """
    while True:
        for ch in range(ps_conn.ch_count + 1):
            raw_data = await ps_conn.get_ch_measures(ch)
            # data = await get_ch_measures_data(ch, raw_data)
            # todo log data with time

        await asyncio.sleep(10)
