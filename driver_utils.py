from power_source_utils import PowerSupplyConnector


class PSCommandsHandler:
    """
    команды и запросы для тестирования источника
    метод для регулярного запроса состояния
    кастомное оформление вывода

    декоратор для логирования в файл рег.опросов сделать рядом

    асинк?
    """
    def __init__(self):
        self.ps_conn = PowerSupplyConnector()
        self.ps_conn.connect()  # todo disconnect

    def get_conditions(self):
        return {}

    def channel_on(self, channel_number, voltage, current):
        pass

    def channel_off(self, channel_number):
        pass

