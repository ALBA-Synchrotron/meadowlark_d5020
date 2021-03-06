# -*- coding: utf-8 -*-
#
# This file is part of the Meadowlark D5020 project
#
# Copyright (c) 2021 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more info.

"""Tango server module for Meadowlark D5020."""

from .meadowlark_d5020 import Meadowlark_d5020


def main():
    import sys
    import logging
    import tango.server
    args = ['Meadowlark_d5020'] + sys.argv[1:]
    fmt = '%(asctime)s %(threadName)s %(levelname)s %(name)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    tango.server.run((Meadowlark_d5020,), args=args)
