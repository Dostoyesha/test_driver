import socket


class PowerSupplyConnector:
    """TCP/IP  SCPI
    комманды самому источнику питания
    сбор команды согласно протоколу в нужном формате

    except
    log
    """

    def __init__(self):
        # self.__resource = "TCPIP0::169.254.129.17::1026::SOCKET"
        self.ch_count = 4   # todo в инит аргумент или конфиг
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    async def connect(self):
        self._s.connect(('127.0.0.1', 9090))
        # self._s.connect(('169.254.129.17', 1026))   # todo

    async def disconnect(self):
        self._s.close()

    async def get_ch_measures(self, ch_number):
        self._s.sendall(f':MEASure{ch_number}:ALL?\n'.encode())
        return self._s.recv(4096)

    async def set_current(self, ch_number, current):
        # :SOURce2:CURRent 1.0005
        self._s.sendall(f':SOURce{ch_number}:CURRent {current}\n'.encode())

    async def set_voltage(self, ch_number, voltage):
        self._s.sendall(f':SOURce{ch_number}:VOLTage {voltage}\n'.encode())

    async def turn_on_ch_output(self, ch_number):
        self._s.sendall(f':OUTPut{ch_number}:STATe ON\n'.encode())

    async def turn_off_ch_output(self, ch_number):
        self._s.sendall(f':OUTPut{ch_number}:STATe OFF\n'.encode())


