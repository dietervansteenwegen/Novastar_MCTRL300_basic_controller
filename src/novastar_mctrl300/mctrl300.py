# -*- coding: utf-8 -*-
"""
Request/command:


"""
from typing import Union


class MCTRL300Msg:
    def __init__(self):
        self.msg: dict = {
            '1_header': [None, None],
            '2_ack': None,
            '3_ser_no_cmd': None,
            '4_scr_addr': None,
            '5_dest_addr': None,
            '6_card_type': None,
            '7_port_addr': bytes(0x00),
            '8_board_addr': bytes([0xFF, 0xFF]),
            '9_cmd_type': None,
            '10_reserved': 0x00,
            '11_register': [None, None, None, None],
            '12_data_length': [None, None],
            '13_data': None,
            'checksum': None,
        }

    def from_string(self, str_cmd):
        bytes_cmd = bytearray.fromhex(str_cmd)
        self.msg['1_header'] = bytes_cmd[:2]
        self.msg['2_ack'] = bytes_cmd[2]
        self.msg['3_ser_no_cmd'] = bytes_cmd[3]
        self.msg['4_scr_addr'] = bytes_cmd[4]
        self.msg['5_dest_addr'] = bytes_cmd[5]
        self.msg['6_card_type'] = bytes_cmd[6]
        self.msg['7_port_addr'] = bytes_cmd[7]
        self.msg['8_board_addr'] = bytes_cmd[8:10]
        self.msg['9_cmd_type'] = bytes_cmd[10:12]
        # self.msg['11_register'] = bytes_cmd[]
        for i in self.msg:
            print(f'{i}: {self.msg[i]}, {type(self.msg[i])}')


class MCTRL300:
    def __init__(self, serport):
        self.serport = serport

    @staticmethod
    def translate_data(data: str):
        lst_data: list = data.split(' ')

        print(f'Header: {lst_data[:2]} (should be 55 AA for cmd, AA 55 for reply')
        print(f'ACK: {lst_data[2]}')
        print(f'serial no/ CMD: {lst_data[3]}')
