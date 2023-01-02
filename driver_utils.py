import asyncio


def log_params(func):
    async def wrapper(*args, **kwargs):
        print("Time now is 0000")
        return await func(*args, **kwargs)
    return wrapper


class PSCommandsHandler:
    """
    команды и запросы для тестирования источника
    кастомное оформление вывода

    декоратор для логирования в файл рег.опросов сделать рядом

    """
    def __init__(self, conn):
        self.conn = conn

    def _prepare_conditions_data(self, data):
        result = {}
        pass
        return result

    async def get_conditions(self):
        raw_data = self.conn.get_conditions()
        return self._prepare_conditions_data(raw_data)

    async def channel_on(self, channel_number, voltage, current):
        pass

    async def channel_off(self, channel_number):
        pass


@log_params
async def get_condition():
    while True:
        print("Condition from power supply is U, I, P")
        await asyncio.sleep(5)
