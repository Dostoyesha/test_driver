import socket


class PowerSupplyConnector:
    """TCP/IP  SCPI
    комманды самому источнику питания
    сбор команды согласно протоколу в нужном формате
    """

    def __init__(self):
        # self.__resource = "TCPIP0::169.254.129.17::1026::SOCKET"
        self._ch_count = 4
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    async def connect(self):
        self._s.connect(('169.254.129.17', 1026))  # todo except

    async def disconnect(self):
        self._s.close()

    async def get_ch_measures(self, channel_number):
        self._s.sendall(f':MEASure{channel_number}:ALL?'.encode())
        return self._s.recv(4096)

    async def get_all_ch_measures(self):
        result = {}

        for ch in range(1, self._ch_count + 1):
            result[ch] = await self.get_ch_measures(ch)

        return result

    async def channel_on(self):
        pass

    async def channel_off(self):
        pass


