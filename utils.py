import asyncio
import datetime

from config import TELEMETRY_REQUEST_TASK_SEC_PERIOD, TELEMETRY_LOG_FILE_PATH


def parse_ch_measures(raw_data):
    """
    :param raw_data: '4.10466677,-3.13684184,1.75743178\n'
    :return:
        {'current': 4.10466677,
        'voltage': -3.13684184,
        'power': 1.75743178}
    """
    result = {}

    if raw_data:
        measures = [float(measure) for measure in raw_data.strip('\n :,').split(',')]

        if measures and len(measures) == 3:
            result['current'] = measures[0]
            result['voltage'] = measures[1]
            result['power'] = measures[2]

    return result


def prepare_ch_measures_data(ch, raw_data):
    result = {'channel': ch}

    measures = parse_ch_measures(raw_data)
    result.update(measures)

    return result


def prepare_condition_data(ch_measures_map):
    """
    :param ch_measures_map: dict with key - channel number, value - measures data from ps
        {1: '4.10466677,-3.13684184,1.75743178\n',
        ..}

    :returns list of dicts with measures of channel
        {'conditions': [
            {'channel': 1,
            'current': 4.10466677,
            'voltage': -3.13684184,
            'power': 1.75743178},
            ..]
        }

    """
    conditions = [prepare_ch_measures_data(ch, data) for ch, data in ch_measures_map.items()]
    return {'conditions': conditions}


def log_ch_measures(func):

    async def wrapper(*args, **kwargs):
        time = datetime.datetime.now()
        ch = args[1]

        result = await func(*args, **kwargs)

        try:
            data = parse_ch_measures(result)

            current, voltage, power = data['current'], data['voltage'], data['power']
            message = f'CURRENT {current}, VOLTAGE {voltage}, POWER {power}'
        except Exception as e:
            message = f'Error by measures getting. Invalid data from PS: {result}'

        log = f'TIME {time}:  CH {ch}:  {message}\n'

        with open(TELEMETRY_LOG_FILE_PATH, 'a') as f:
            f.write(log)

        return result
    return wrapper


async def task_get_condition(ps_conn):
    while True:
        for ch in range(1, ps_conn.ch_count + 1):
            await ps_conn.get_ch_measures(ch)

        await asyncio.sleep(TELEMETRY_REQUEST_TASK_SEC_PERIOD)
