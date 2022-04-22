# -*- coding: utf-8 -*-
from typing import List

import desay6_upad26_ctrl.desay6_upad26_LED as LED
import serial.serialutil
from PyQt5 import QtWidgets
from serports import serports

from .main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._refresh_serial_ports()
        self.btn_serial_refresh.clicked.connect(self._refresh_serial_ports)
        self.btn_serial_open.clicked.connect(lambda checked: self._open_serial_port(checked))
        self.serport = None
        self.cmb_output.currentIndexChanged.connect(lambda index: self._output_changed(index))
        self.led_screen = None

    def _output_changed(self, index: int):
        # TODO: if serial port changes, self.led_screen does not get updated with the new port
        # TODO: change so that first you need to select port, then output, then controls are shown
        if index == 0 or self.serport is None:
            self.led_screen = None
        elif index == 1:
            self.led_screen = LED.Out1(self.serport)
        elif index == 2:
            self.led_screen = LED.Out2(self.serport)

    def _refresh_serial_ports(self) -> None:
        self.lst_serial_ports.clear()
        self.serial_available_ports: List = []
        for port in sorted(serports.get_available_ports()):
            self.serial_available_ports.append(port)
            self.lst_serial_ports.addItem(f' {port[1]}  ({port[2]}, {port[3]})')
        if len(self.serial_available_ports) > 0:
            self.btn_serial_open.setEnabled(True)
            self.lst_serial_ports.setCurrentRow(0)
        else:
            self.btn_serial_open.setEnabled(False)
            self.lbl_serial_status.setText('No ports found...')
            self.lbl_serial_status.setStyleSheet('background-color:orange')

    def _open_serial_port(self, checked) -> None:
        if checked:
            if len(self.serial_available_ports) == 0:
                # self.lbl_serial_status.setText('No serial ports')
                self.btn_serial_open.setChecked(False)
                return
            index = self.lst_serial_ports.currentRow()
            try:
                self.serport = serports.Mctrl300Serial(self.serial_available_ports[index][1])
            except (FileNotFoundError, serial.serialutil.SerialException) as e:
                # TODO: add logging to file and option to open logfile
                print(e)
                self._refresh_serial_ports()
                self.btn_serial_open.setChecked(False)
            if self.serport and self.serport.isOpen():
                self.lbl_serial_status.setText(f'Opened {self.serial_available_ports[index][1]}')
                self.btn_serial_open.setText(
                    f'Click to close {self.serial_available_ports[index][1]}', )
                self.lbl_serial_status.setStyleSheet('background-color:green')
            else:
                self.lbl_serial_status.setText('Error opening port. See logs.')
                self.lbl_serial_status.setStyleSheet('background-color:red')
                self.serport = None
        else:
            if self.serport:
                self.serport.close()
            self.lbl_serial_status.setText('Closed serial port')
            self.lbl_serial_status.setStyleSheet('background-color:orange')
            self.btn_serial_open.setText('Click to open selected port')


def start_gui():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
