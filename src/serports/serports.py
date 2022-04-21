# -*- coding: utf-8 -*-
import serial
from serial.tools import list_ports

BAUDRATE = 115200
TIMEOUT = 4


def get_available_ports() -> list:
    ports = list_ports.comports(include_links=False)
    return ([(i, port.device, port.manufacturer, port.product) for i, port in enumerate(ports)])


class Mctrl300Serial(serial.Serial):
    def __init__(self, port: str):
        super().__init__(
            port,
            baudrate=BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=TIMEOUT,
        )
        self.write('test\n'.encode())
