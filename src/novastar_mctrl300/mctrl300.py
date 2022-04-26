#! /usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Dieter Vansteenwegen'
__project__ = 'Novastar_MCTRL300_basic_controller'
__project_link__ = 'https://github.com/dietervansteenwegen/desay6mm_upad2mm6_ctrl'

import serial
from typing import Union, List

BAUDRATE = 115200
TIMEOUT = 4


class MCTRL300:
    def __init__(self, serport: serial.Serial):
        # self.log = initialize_logger()
        self._init_serport(serport)

    def _init_serport(self, serport: serial.Serial):
        self.serport = serport


class MCTRL300Msg:
    def __init__(self):
        self.msg = bytearray()

    def generate(
        self,
        serno: int,
        reg_addr: List[int],
        data_len: int,
        data: Union[int, List[int]],
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


class Out1(MCTRL300):
    """Class for output 1.

    Args:
        serport (str): name of the serial port device connected to the controller.
                    e.g. 'com1' in Windows, '/dev/ttyUSB1' in Linux
    """
    # fixed known commands
    NORMAL_6 = bytes.fromhex('55 aa 00 23 FE 00 01 00 FF FF 01 00 01 01 00 02 01 00 01 7C 58')
    RED_6 = bytes.fromhex('55 aa 00 2E FE 00 01 00 FF FF 01 00 01 01 00 02 01 00 02 88 58')
    GREEN_6 = bytes.fromhex('55 aa 00 41 FE 00 01 00 FF FF 01 00 01 01 00 02 01 00 03 9C 58')
    BLUE_6 = bytes.fromhex('55 aa 00 4B FE 00 01 00 FF FF 01 00 01 01 00 02 01 00 04 A7 58')
    WHITE_6 = bytes.fromhex('55 aa 00 17 FE 00 01 00 FF FF 01 00 01 01 00 02 01 00 05 74 58')
    SLASH_6 = bytes.fromhex('55 aa 00 4F FE 00 01 00 FF FF 01 00 01 01 00 02 01 00 08 AF 58')

    def __init__(self, serport: serial.Serial):
        super().__init__(serport)

    def normal(self) -> None:
        """Display the normal pattern (=video input or black if no source)."""
        self.serport.write(self.NORMAL_6)

    def red(self) -> None:
        """Display the red pattern."""
        self.serport.write(self.RED_6)

    def green(self) -> None:
        """Display the green pattern."""
        self.serport.write(self.GREEN_6)

    def blue(self) -> None:
        """Display the blue pattern."""
        self.serport.write(self.BLUE_6)

    def white(self) -> None:
        """Display the white pattern."""
        self.serport.write(self.WHITE_6)

    def slash(self) -> None:
        """Display the slash (moving diagonal lines) pattern."""
        self.serport.write(self.SLASH_6)

    def black(self) -> None:
        """Display a black screen."""
        raise NotImplementedError()

    def freeze(self) -> None:
        """Freeze the screen."""
        raise NotImplementedError('Still need to capture cmd for freeze.')

    def send_msg(self, msg) -> None:
        self.serport.write(msg)

    def set_brightness(self, value: int):
        msg = MCTRL300Msg()
        cmd = msg.generate(serno=0x15, reg_addr=[0x2, 0, 0, 1], data_len=1, data=value)
        self.serport.write(cmd)


class Out2(MCTRL300):
    """Class for output 2.

    Args:
        serport (str): name of the serial port device connected to the controller.
                    e.g. 'com1' in Windows, '/dev/ttyUSB1' in Linux
    """
    # fixed known commands
    NORMAL_26 = bytes.fromhex('55 aa 00 67 FE 00 01 01 FF FF 01 00 01 01 00 02 01 00 01 C1 58')
    RED_26 = bytes.fromhex('55 aa 00 54 FE 00 01 01 FF FF 01 00 01 01 00 02 01 00 02 AF 58')
    GREEN_26 = bytes.fromhex('55 aa 00 74 FE 00 01 01 FF FF 01 00 01 01 00 02 01 00 03 D0 58')
    BLUE_26 = bytes.fromhex('55 aa 00 85 FE 00 01 01 FF FF 01 00 01 01 00 02 01 00 04 E2 58')
    # WHITE_26 = bytes.fromhex('55 aa 00 2b fe 00 00 00 00 00 00 00 02 00 00 00 02 00 82 56')
    SLASH_26 = bytes.fromhex('55 aa 00 8F FE 00 01 01 FF FF 01 00 01 01 00 02 01 00 08 F0 58')

    def __init__(self, serport: serial.Serial):
        super().__init__(serport)

    def normal(self) -> None:
        """Display the normal pattern (=video input or black if no source)."""
        self.serport.write(self.NORMAL_26)

    def red(self) -> None:
        """Display the red pattern."""
        self.serport.write(self.RED_26)

    def green(self) -> None:
        """Display the green pattern."""
        self.serport.write(self.GREEN_26)

    def blue(self) -> None:
        """Display the blue pattern."""
        self.serport.write(self.BLUE_26)

    def white(self) -> None:
        """Display the white pattern."""
        # self.serport.write(self.WHITE_26)
        raise NotImplementedError(
            'Still need to capture the command to display the white pattern'
            'on the UPAD 2.6mm', )

    def slash(self) -> None:
        """Display the slash (moving diagonal lines) pattern."""
        self.serport.write(self.SLASH_26)

    def black(self) -> None:
        """Display a black screen."""
        raise NotImplementedError('Still need to capture cmd for black.')

    def freeze(self) -> None:
        """Freeze the screen."""
        raise NotImplementedError('Still need to capture cmd for freeze.')


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

if __name__ == '__main__':
    s = msg_gen()
    s.gen(serno=0x15, reg_addr=[0x2, 0, 0, 1], data_len=1, data=0x80)
