import socket

from config import POWER_SUPPLY_HOST, POWER_SUPPLY_PORT
from utils import log_ch_measures


class PowerSupplyConnector:
    """TCP/IP connector to Power Supply with SCPI commands."""

    def __init__(self, ch_count):
        self.ch_count = ch_count
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self._s.connect((POWER_SUPPLY_HOST, POWER_SUPPLY_PORT))

    def disconnect(self):
        self._s.close()

    def _set_command(self, raw_command):
        return f'{raw_command}\n'.encode()

    def _send_command(self, raw_command):
        command = self._set_command(raw_command)
        self._s.sendall(command)

    @log_ch_measures
    async def get_ch_measures(self, ch_number):
        self._send_command(f':MEASure{ch_number}:ALL?')
        return self._s.recv(4096).decode()

    async def set_current(self, ch_number, current):
        self._send_command(f':SOURce{ch_number}:CURRent {current}')

    async def set_voltage(self, ch_number, voltage):
        self._send_command(f':SOURce{ch_number}:VOLTage {voltage}')

    async def turn_on_ch_output(self, ch_number):
        self._send_command(f':OUTPut{ch_number}:STATe ON')

    async def turn_off_ch_output(self, ch_number):
        self._send_command(f':OUTPut{ch_number}:STATe OFF')
