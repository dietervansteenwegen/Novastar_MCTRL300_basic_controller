# -*- coding: utf-8 -*-
from typing import List

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
        self.cmb_output.setCurrentIndex(1)

    def _refresh_serial_ports(self) -> None:
        self.lst_serial_ports.clear()
        self.serial_available_ports: List = []
        for port in sorted(serports.get_available_ports()):
            self.serial_available_ports.append(port)
            self.lst_serial_ports.addItem(f' {port[1]}  ({port[2]}, {port[3]})')
        if len(self.serial_available_ports) > 0:
            self.btn_serial_open.setEnabled(True)
        else:
            self.btn_serial_open.setEnabled(False)
            self.lbl_serial_status.setText('No ports found...')

    def _open_serial_port(self, checked) -> None:
        if checked:
            if len(self.serial_available_ports) == 0:
                self.lbl_serial_status.setText('No serial ports')
                self.btn_serial_open.setChecked(False)
                return
            index = self.lst_serial_ports.currentRow()
            self.serport = serports.Mctrl300Serial(self.serial_available_ports[index][1])
            if self.serport.isOpen():
                self.lbl_serial_status.setText(f'Opened {self.serial_available_ports[index][1]}')
            else:
                self.lbl_serial_status.setText(
                    f'Error opening {self.serial_available_ports[index][1]}. See logs.',
                )
                self.serport = None

        else:
            if self.serport:
                self.serport.close()
            self.lbl_serial_status.setText('Closed serial port')


def start_gui():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
