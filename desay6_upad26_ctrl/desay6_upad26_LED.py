#! /usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Dieter Vansteenwegen'
__project__ = 'Desay 6mm and UPAD 2.6mm test pattern control'
__project_link__ = 'https://github.com/dietervansteenwegen/desay6mm_upad2mm6_ctrl'

import logging
import serial

BAUDRATE = 115200
TIMEOUT = 4


def initialize_logger() -> logging.Logger:
    """Set up logger
    If the module is ran as a module, name logger accordingly as a sublogger.
    Returns:
        logging.Logger: logger instance
    """
    if __name__ == '__main__':
        return logging.getLogger(f'{__name__}')
    else:
        return logging.getLogger(f'__main__.{__name__}')


class LedScreen:
    def __init__(self, serport: str):
        self.log = initialize_logger()
        self._init_serport(serport)

    def _init_serport(self, serport: str):
        self.serport = serial.Serial(
            serport,
            BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=TIMEOUT,
        )


class Desay6(LedScreen):
    NORMAL_6 = bytes.fromhex('55 aa 00 23 FE 00 01 00 FF FF 01 00 01 01 00 02 01 00 01 7C 58')
    RED_6 = bytes.fromhex('55 aa 00 2E FE 00 01 00 FF FF 01 00 01 01 00 02 01 00 02 88 58')
    GREEN_6 = bytes.fromhex('55 aa 00 41 FE 00 01 00 FF FF 01 00 01 01 00 02 01 00 03 9C 58')
    BLUE_6 = bytes.fromhex('55 aa 00 4B FE 00 01 00 FF FF 01 00 01 01 00 02 01 00 04 A7 58')
    WHITE_6 = bytes.fromhex('55 aa 00 17 FE 00 01 00 FF FF 01 00 01 01 00 02 01 00 05 74 58')
    SLASH_6 = bytes.fromhex('55 aa 00 4F FE 00 01 00 FF FF 01 00 01 01 00 02 01 00 08 AF 58')

    def __init__(self, serport: str):
        super().__init__(serport)

    def normal(self):
        self.serport.write(self.NORMAL_6)

    def red(self):
        self.serport.write(self.RED_6)

    def green(self):
        self.serport.write(self.GREEN_6)

    def blue(self):
        self.serport.write(self.BLUE_6)

    def white(self):
        self.serport.write(self.WHITE_6)

    def slash(self):
        self.serport.write(self.SLASH_6)


class Upad26(LedScreen):
    NORMAL_26 = bytes.fromhex('55 aa 00 67 FE 00 01 01 FF FF 01 00 01 01 00 02 01 00 01 C1 58')
    RED_26 = bytes.fromhex('55 aa 00 54 FE 00 01 01 FF FF 01 00 01 01 00 02 01 00 02 AF 58')
    GREEN_26 = bytes.fromhex('55 aa 00 74 FE 00 01 01 FF FF 01 00 01 01 00 02 01 00 03 D0 58')
    BLUE_26 = bytes.fromhex('55 aa 00 85 FE 00 01 01 FF FF 01 00 01 01 00 02 01 00 04 E2 58')
    # WHITE_26 = bytes.fromhex('55 aa 00 2b fe 00 00 00 00 00 00 00 02 00 00 00 02 00 82 56')
    SLASH_26 = bytes.fromhex('55 aa 00 8F FE 00 01 01 FF FF 01 00 01 01 00 02 01 00 08 F0 58')

    def __init__(self, serport: str):
        super().__init__(serport)

    def normal(self):
        self.serport.write(self.NORMAL_26)

    def red(self):
        self.serport.write(self.RED_26)

    def green(self):
        self.serport.write(self.GREEN_26)

    def blue(self):
        self.serport.write(self.BLUE_26)

    def white(self):
        self.serport.write(self.WHITE_26)

    def slash(self):
        self.serport.write(self.SLASH_26)
