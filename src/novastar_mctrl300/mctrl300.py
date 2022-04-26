# -*- coding: utf-8 -*-
"""
Request/command:


"""
from typing import Union

# class MCTRL300Msg:
#     def __init__(self):
#         self.msg: dict = {
#             '1_header': [None, None],
#             '2_ack': None,
#             '3_ser_no_cmd': None,
#             '4_scr_addr': None,
#             '5_dest_addr': None,
#             '6_card_type': None,
#             '7_port_addr': bytes(0x00),
#             '8_board_addr': bytes([0xFF, 0xFF]),
#             '9_cmd_type': None,
#             '10_reserved': 0x00,
#             '11_register': [None, None, None, None],
#             '12_data_length': [None, None],
#             '13_data': None,
#             'checksum': None,
#         }

#     def from_string(self, str_cmd):
#         bytes_cmd = bytearray.fromhex(str_cmd)
#         self.msg['1_header'] = bytes_cmd[:2]
#         self.msg['2_ack'] = bytes_cmd[2]
#         self.msg['3_ser_no_cmd'] = bytes_cmd[3]
#         self.msg['4_scr_addr'] = bytes_cmd[4]
#         self.msg['5_dest_addr'] = bytes_cmd[5]
#         self.msg['6_card_type'] = bytes_cmd[6]
#         self.msg['7_port_addr'] = bytes_cmd[7]
#         self.msg['8_board_addr'] = bytes_cmd[8:10]
#         self.msg['9_cmd_type'] = bytes_cmd[10:12]
#         # self.msg['11_register'] = bytes_cmd[]
#         for i in self.msg:
#             print(f'{i}: {self.msg[i]}, {type(self.msg[i])}')


class msg_gen:
    def __init__(self):
        self.msg = bytearray()

    def gen(
        self,
        serno: int,
        reg_addr: 'list[int]',
        data_len: int,
        data: Union[int, 'list[int]'],
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
        self._append_port_addr()
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
        print('msg:', end='')
        for i in self.msg:
            print(f'{hex(i)} ', end=' ')
        print()

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
        for i in reversed(reg_addr):
            self.msg.append(i)

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

    def _append_port_addr(self):
        self.msg.append(0x00)

    def _append_board_addr(self):
        for i in [0x00, 0x00]:
            self.msg.append(i)

    def _append_cmd_type(self, is_write):
        self.msg.append(0x01 if is_write else 0x00)

    def _append_reserved(self):
        self.msg.append(0x00)


if __name__ == '__main__':
    s = msg_gen()
    s.gen(serno=0x15, reg_addr=[0x2, 0, 0, 1], data_len=1, data=0x80)
