

class PowerSupplyConnector:
    """TCP/IP  SCPI
    комманды самому источнику питания
    сбор команды согласно протоколу в нужном формате
    """

    def __init__(self):
        self.resource = "TCPIP0::169.254.129.17::1026::SOCKET"

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def get_condition(self):
        pass

    async def channel_on(self):
        pass

    async def channel_off(self):
        pass


