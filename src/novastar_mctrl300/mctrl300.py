#! /usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Dieter Vansteenwegen'
__project__ = 'Novastar_MCTRL300_basic_controller'
__project_link__ = 'https://github.com/dietervansteenwegen/desay6mm_upad2mm6_ctrl'

import serial
from typing import Union, List
from serports import Mctrl300Serial

BAUDRATE = 115200
TIMEOUT = 4


class MCTRL300:
    REG_TEST_PATTERN = 0x02000101
    REG_BRIGHTNESS_OVERALL = 0x02000001

    PATTERN_NORMAL = 1
    PATTERN_RED = 2
    PATTERN_GREEN = 3
    PATTERN_BLUE = 4
    PATTERN_WHITE = 5
    PATTERN_HORIZONTAL = 6
    PATTERN_VERTICAL = 7
    PATTERN_SLASH = 8
    PATTERN_GRAYSCALE = 9

    def __init__(self, serport: serial.Serial):
        # self.log = initialize_logger()
        self._init_serport(serport)
        self._msg_id: int = 0  # increasing number for each message sent
        self.output = 0
        self.creator = MCTRL300CreateCommand()

    def _init_serport(self, serport: serial.Serial):
        self.serport = serport

    def set_pattern(self, pattern: int, port: int):
        cmd = self.creator.generate(
            serno=self._msg_id,
            port=port,
            reg_addr=self.REG_TEST_PATTERN,
            data_len=1,
            data=pattern,
        )
        self._print_cmd(cmd)
        self._send_cmd(cmd)

    def _print_cmd(self, cmd):
        print('cmd: ', end='')
        for i in cmd:
            print(hex(i), end=' ')
        print()

    def set_brightness(self, port: int, value: int):
        cmd = self.creator.generate(
            serno=self._msg_id,
            port=port,
            reg_addr=self.REG_BRIGHTNESS_OVERALL,
            data_len=1,
            data=value,
        )
        self._send_cmd(cmd)

    def _send_cmd(self, cmd):
        self.serport.write(cmd)
        self._msg_id += 1


class MCTRL300CreateCommand:
    def __init__(self):
        self.msg = bytearray()

    def generate(
        self,
        serno: int,
        reg_addr: int,
        data_len: int,
        data: Union[int, List[int]],
        port: int,
        is_cmd: bool = True,
        is_write: bool = True,
        ack=0,
    ):
        self.msg = bytearray()
        self._append_header(is_cmd)
        self._append_ack(ack)
        self.msg.append(serno)
        self._append_src()
        self._append_dest()
        self._append_card_type()
        self._append_port_addr(port)
        self._append_board_addr()
        self._append_cmd_type(is_write)
        self._append_reserved()
        self._append_reg_addr(reg_addr)
        self._append_data_len(data_len)
        self._append_data(data)
        self._append_checksum()
        return self.msg

    def _append_ack(self, ack):
        self.msg.append(ack)

    def _append_checksum(self):
        c = sum(self.msg[3:])
        c += 0x5555
        self.msg.append(c & 0xFF)
        self.msg.append(c >> 8)

    def _append_data(self, data):
        if type(data) == list:
            self.msg.append(*data)
        else:
            self.msg.append(data)

    def _append_data_len(self, data_len):
        # TODO: support data len > 255
        self.msg.append(data_len)
        self.msg.append(0)

    def _append_reg_addr(self, reg_addr):
        self.msg.append(reg_addr & 0xFF)
        self.msg.append((reg_addr & 0x0000FF00) >> 8)
        self.msg.append((reg_addr & 0x00FF0000) >> 16)
        self.msg.append((reg_addr & 0xFF000000) >> 24)

    def _append_header(self, is_cmd):
        header = [0x55, 0xAA] if is_cmd else [0xAA, 0x55]
        for i in header:
            self.msg.append(i)  # header

    def _append_src(self):
        self.msg.append(0xFE)

    def _append_dest(self):
        self.msg.append(0x00)

    def _append_card_type(self):
        # 00 for sender, 01 for receiver, 02 for function
        self.msg.append(0x01)

    def _append_port_addr(self, port):
        self.msg.append(port - 1)

    def _append_board_addr(self):
        for i in [0xFF, 0xFF]:
            self.msg.append(i)

    def _append_cmd_type(self, is_write):
        self.msg.append(0x01 if is_write else 0x00)

    def _append_reserved(self):
        self.msg.append(0x00)


if __name__ == '__main__':
    p = Mctrl300Serial('/dev/ttyUSB0')
    s = MCTRL300(p)
    s.set_pattern(MCTRL300.PATTERN_RED, 1)
    s.set_brightness(1, 0x10)
