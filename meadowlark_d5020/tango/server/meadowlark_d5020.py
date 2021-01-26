# -*- coding: utf-8 -*-
#
# This file is part of the Meadowlark D5020 project
#
# Copyright (c) 2021 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more info.

"""Tango server class for Meadowlark_d5020"""

import asyncio
import urllib.parse

from connio import connection_for_url
from tango import GreenMode
from tango.server import Device, attribute, command, device_property

import meadowlark_d5020.core


class Meadowlark_d5020(Device):

    green_mode = GreenMode.Asyncio

    url = device_property(dtype=str)

    async def init_device(self):
        await super().init_device()
        self.connection = connection_for_url(self.url, concurrency="async")
        self.meadowlark_d5020 = meadowlark_d5020.core.Meadowlark_d5020(self.connection)

    @attribute(dtype=str, label="ID")
    def idn(self):
        return self.meadowlark_d5020.get_idn()

    @attribute(dtype=float, unit="bar", label="Pressure")
    async def pressure(self):
        # example processing the result
        pressure = await self.meadowlark_d5020.get_pressure()
        return pressure / 1000

    @attribute(dtype=float, unit="bar", label="Pressure set point")
    async def pressure_setpoint(self):
        # example processing the result
        setpoint = await self.meadowlark_d5020.get_pressure_setpoint()
        return setpoint / 1000

    @pressure_setpoint.setter
    def pressure_setpoint(self, value):
        # example returning the coroutine back to tango
        return self.meadowlark_d5020.get_pressure_setpoint(value * 1000)

    @command
    def turn_on(self):
        # example returning the coroutine back to who calling function
        return self.meadowlark_d5020.turn_on()


if __name__ == "__main__":
    import logging
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level="DEBUG", format=fmt)
    Meadowlark_d5020.run_server()
