import socket

from config import POWER_SUPPLY_HOST, POWER_SUPPLY_PORT
from utils import log_ch_measures


class PowerSupplyConnector:
    """TCP/IP connector to Power Supply with SCPI commands."""

    def __init__(self, ch_count):
        self.ch_count = ch_count
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self._s.connect((POWER_SUPPLY_HOST, POWER_SUPPLY_PORT))  # todo try except

    def disconnect(self):
        self._s.close()

    @log_ch_measures
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


