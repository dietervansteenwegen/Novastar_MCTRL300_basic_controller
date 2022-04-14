#! /usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Dieter Vansteenwegen'
__project__ = 'Desay 6mm and UPAD 2.6mm test pattern control'
__project_link__ = 'https://github.com/dietervansteenwegen/desay6mm_upad2mm6_ctrl'

import logging


def initialize_logger() -> logging.Logger:
    """Set up logger
    If the module is ran as a module, name logger accordingly as a sublogger.
    Returns:
        logging.Logger: logger instance
    """
    if __name__ == '__main__':
        return logging.getLogger('{}'.format(__name__))
    else:
        return logging.getLogger('__main__.{}'.format(__name__))


class ADCNotImplemented(NotImplementedError):
    """Info here."""
    pass


class pPTHEAD:
    pass
