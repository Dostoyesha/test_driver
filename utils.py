import asyncio


def log_ch_measures(func):
    async def wrapper(*args, **kwargs):
        await func(*args, **kwargs)
        print("Time now is 0000")  # todo to file
    return wrapper


async def get_ch_measures_data(ch, raw_data):
    """
    :param ch:
    :param raw_data: 'some U I P data'
    :return: {'channel': '1',
        'current': '1.0001',
        'voltage': '2.0002',
        'power': '3'}
    """
    # todo
    return {'channel': '1',
            'current': '1.0001',
            'voltage': '2.0002',
            'power': '3'}


async def prepare_condition_data(ch_measures_map):
    """
    :param ch_measures_map: {1: 'measures data',
                             2: 'measures data'}
    :returns
    [
        {'channel': '1',
        'current': '1.0001',
        'voltage': '2.0002',
        'power': '3'},
    ]
    """
    return [await get_ch_measures_data(ch, data) for ch, data in ch_measures_map]   # todo нужен ли await


async def task_get_condition(ps_conn):
    """
    значение из коннектора или функции их хендлера?
    """
    while True:
        for ch in range(ps_conn.ch_count + 1):
            raw_data = await ps_conn.get_ch_measures(ch)
            data = await get_ch_measures_data(ch, raw_data)
            # todo log data with time

        await asyncio.sleep(10)
