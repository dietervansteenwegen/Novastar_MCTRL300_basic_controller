# -*- coding: utf-8 -*-
from typing import List

import desay6_upad26_ctrl.desay6_upad26_LED as LED
import serial.serialutil
from PyQt5 import QtWidgets
from serports import serports

from .main_window_2 import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._refresh_serial_ports()
        self.serport = None
        self.led_screen = None
        self.state = 1
        self._connect_slots()
        self._update_to_state()
        self._set_up_timer_brightness()

    def _set_up_timer_brightness(self):
        # TODO: Timer querying brightness and setting slider value + label
        # TODO: Code for setting/getting brightness
        pass

    def _connect_slots(self):
        self.btn_serial_refresh.clicked.connect(self._refresh_serial_ports)
        self.btn_serial_open.clicked.connect(lambda checked: self._open_serial_port(checked))
        self.cmb_output.currentIndexChanged.connect(lambda index: self._output_changed(index))
        self.btn_blackout.clicked.connect(self._pattern_black)
        self.btn_blue.clicked.connect(self._pattern_blue)
        self.btn_freeze.clicked.connect(self._pattern_freeze)
        self.btn_green.clicked.connect(self._pattern_green)
        self.btn_normal.clicked.connect(self._pattern_normal)
        self.btn_red.clicked.connect(self._pattern_red)
        self.btn_slash.clicked.connect(self._pattern_slash)
        self.btn_white.clicked.connect(self._pattern_white)
        self.sldr_brightness.sliderMoved.connect(self._brightness_slider_moved)

    def _brightness_slider_moved(self, v):
        # TODO: send out brightness set commands
        self.lbl_brightness_value.setText(str(v))

    def _output_changed(self, index: int):
        if index == 0 or self.serport is None:
            self.led_screen = None
            self._change_state_to(2)
        elif index == 1:
            self.led_screen = LED.Out1(self.serport)
            self._change_state_to(3)
        elif index == 2:
            self.led_screen = LED.Out2(self.serport)
            self._change_state_to(3)

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
            self._change_state_to(1)

    def _open_serial_port(self, checked) -> None:
        if checked:
            if len(self.serial_available_ports) == 0:
                # self.lbl_serial_status.setText('No serial ports')
                self.btn_serial_open.setChecked(False)
                self._change_state_to(1)
                return
            index = self.lst_serial_ports.currentRow()
            try:
                self.serport = serports.Mctrl300Serial(self.serial_available_ports[index][1])
            except (FileNotFoundError, serial.serialutil.SerialException) as e:
                # TODO: add logging to file and option to open logfile
                print(e)
                self._refresh_serial_ports()
                self.btn_serial_open.setChecked(False)
                self._change_state_to(1)
            if self.serport and self.serport.isOpen():
                self.lbl_serial_status.setText(f'Opened {self.serial_available_ports[index][1]}')
                self.btn_serial_open.setText(
                    f'Click to close {self.serial_available_ports[index][1]}', )
                self.lbl_serial_status.setStyleSheet('background-color:green')
                self._change_state_to(2)
            else:
                self.lbl_serial_status.setText('Error opening port. See logs.')
                self.lbl_serial_status.setStyleSheet('background-color:red')
                self.serport = None
                self._change_state_to(1)
        else:
            if self.serport:
                self.serport.close()
            self.lbl_serial_status.setText('Closed serial port')
            self.lbl_serial_status.setStyleSheet('background-color:orange')
            self.btn_serial_open.setText('Click to open selected port')
            self._change_state_to(1)

    def _change_state_to(self, state: int):
        if state == 2 and self.cmb_output.currentIndex() > 0:
            state = 3
        self.state = state
        self._update_to_state()

    def _update_to_state(self):
        self.cmb_output.setEnabled(self.state > 1)
        self.sldr_brightness.setEnabled(self.state > 2)
        self.btn_normal.setEnabled(self.state > 2)
        self.btn_red.setEnabled(self.state > 2)
        self.btn_green.setEnabled(self.state > 2)
        self.btn_blue.setEnabled(self.state > 2)
        self.btn_white.setEnabled(self.state > 2)
        self.btn_slash.setEnabled(self.state > 2)
        self.btn_freeze.setEnabled(self.state > 2)
        self.btn_blackout.setEnabled(self.state > 2)

    def _pattern_red(self):
        if self.led_screen:
            self.led_screen.red()

    def _pattern_blue(self):
        if self.led_screen:
            self.led_screen.blue()

    def _pattern_green(self):
        if self.led_screen:
            self.led_screen.green()

    def _pattern_white(self):
        if self.led_screen:
            self.led_screen.white()

    def _pattern_slash(self):
        if self.led_screen:
            self.led_screen.slash()

    def _pattern_normal(self):
        if self.led_screen:
            self.led_screen.normal()

    def _pattern_black(self):
        if self.led_screen:
            self.led_screen.black()

    def _pattern_freeze(self):
        if self.led_screen:
            self.led_screen.freeze()


def start_gui():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
