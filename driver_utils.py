import asyncio


def log_ch_measures(func):
    async def wrapper(*args, **kwargs):
        await func(*args, **kwargs)
        print("Time now is 0000")  # todo to file
    return wrapper


class PSCommandsHandler:
    """
    верхнеуровненвые команды к источнику
    обработка полученных данных
    кастомное оформление вывода

    except
    log
    """
    def __init__(self, conn):
        self.conn = conn
        self.ch_count = self.conn.ch_count

    async def _prepare_conditions_data(self, data):
        pass

    @log_ch_measures    # todo или лог в регулярной таске
    async def get_ps_condition(self):
        """Get measures for all channels in json"""

        ch_measures_map = {ch: await self.conn.get_ch_measures(ch) for ch in range(1, self.ch_count + 1)}
        result = await self._prepare_conditions_data(ch_measures_map)
        return result

    async def channel_on(self, ch_number, voltage, current):
        self.conn.set_current(ch_number, current)
        self.conn.set_voltage(ch_number, voltage)
        self.conn.turn_on_ch_output(ch_number)

    async def channel_off(self, ch_number):
        self.conn.turn_off_ch_output(ch_number)


@log_ch_measures
async def get_condition():
    """
    значение из коннектора или функции их хендлера?
    :return:
    """
    while True:
        print("Condition from power supply is U, I, P")
        await asyncio.sleep(5)
