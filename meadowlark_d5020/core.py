# -*- coding: utf-8 -*-
#
# This file is part of the Meadowlark D5020 project
#
# Copyright (c) 2021 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more info.

"""
Core Meadowlark_d5020 module.

It can receive an asynchronous connection object. Example::

    from connio import connection_for_url
    from meadowlark_d5020.core import Meadowlark_d5020

    async def main():
        tcp = connection_for_url("tcp://meadowlark_d5020.acme.org:5000")
        meadowlark_d5020 = Meadowlark_d5020(tcp)

        idn = await meadowlark_d5020.get_idn()
        print(idn)

    asyncio.run(main())
"""

from enum import Enum
from serial import Serial


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


class Waveform(Enum):
    invariant = 0
    sinusoid = 1
    triangle = 2
    square = 3
    sawtooth = 4
    TNE = 5
    threshold = 6
    trigger = 7
    external_input = 8


class Meadowlark_d5020:
    """The central Meadowlark_d5020"""

    _conn = None

    # Min and Max values
    MIN_VOLTAGE = 0
    MAX_VOLTAGE = 10000

    MAX_PHASE = 360

    MIN_PERIOD = 5
    MAX_PERIOD = 65535

    MIN_DUTY_CICLE = 0
    MAX_DUTY_CICLE = 100

    MIN_TNE_TIME = 0
    MAX_TNE_TIME = 255

    dict_waveform = {
        0:  "inv", 1:  "sin", 2:  "tri", 3:  "sqr",
        4:  "saw", 5:  "tnew", 6:  "thr", 7:  "trg", 8:  "extin"}

    command_waveform = {
        0: "{}:{},{}\n",  # inv
        1: "{}:{},{},{},{},{}\n",  # sin
        2: "{}:{},{},{},{},{}\n",  # saw
        3: "{}:{},{},{},{},{}\n",  # tri
        4: "{}:{},{},{},{},{},{}\n",  # sqr
        5: "{}:{},{},{},{},{},{},{},{}\n",  # tnew
        6: "{}:{},{},{}\n",  # thr
        7: "{}:{}\n",  # trg -> doc: trg:n,?<CR>
        8: "{}:{}\n",  # extin
    }

    def __init__(self, number: int, conn: Serial):
        # Channel number
        self.number = number
        if Meadowlark_d5020._conn is None:
            Meadowlark_d5020._conn = conn
        else:
            print("Using previous serial connection.")

        # Default parameters of the Channel
        self.__waveform = 0
        self.__v1 = 0
        self.__v2 = 1000
        self.__period_t = 1000
        self.__phase = 0
        self.__duty_cycle = 0
        # Parameters of Transient Nematic Effect
        self.__tne_voltage = 0
        self.__tne_time = 0

        # Others
        self.__external_input = False

    ###########################################################################

    @property
    def waveform(self):
        return self.__waveform

    @waveform.setter
    def waveform(self, value: Waveform):
        self.__waveform = value
        self.update_device()

    ###########################################################################

    @property
    def v1(self):
        return self.__v1

    @v1.setter
    def v1(self, value):
        self.__v1 = clamp(value, self.MIN_VOLTAGE, self.MAX_VOLTAGE)
        self.update_device()

    ###########################################################################

    @property
    def v2(self):
        return self.__v2

    @v2.setter
    def v2(self, value):
        self.__v2 = clamp(value, self.MIN_VOLTAGE, self.MAX_VOLTAGE)
        self.update_device()

    ###########################################################################

    @property
    def period(self):
        return self.__period_t

    @period.setter
    def period(self, value):
        self.__period_t = clamp(value, self.MIN_PERIOD, self.MAX_PERIOD)
        self.update_device()

    ###########################################################################

    @property
    def phase(self):
        return self.__phase

    @phase.setter
    def phase(self, value):
        self.__phase = value % self.MAX_PHASE
        self.update_device()

    ###########################################################################

    @property
    def duty_cycle(self):
        return self.__duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, value):
        self.__duty_cycle = clamp(
            value, self.MIN_DUTY_CICLE, self.MAX_DUTY_CICLE)
        self.update_device()

    ###########################################################################

    @property
    def tne_voltage(self):
        return self.__tne_voltage

    @tne_voltage.setter
    def tne_voltage(self, value):
        self.__tne_voltage = clamp(
            value, self.MIN_VOLTAGE, self.MAX_VOLTAGE)
        self.update_device()

    ###########################################################################

    @property
    def tne_time(self):
        return self.__tne_time

    @tne_time.setter
    def tne_time(self, value):
        self.__tne_time = clamp(
            value, self.MIN_TNE_TIME, self.MAX_TNE_TIME)
        self.update_device()

    ###########################################################################

    @property
    def external_input(self):
        return self.__external_input

    def toggle_external_input(self):
        # TODO: Check if sending this command twice disable the external input.
        self.__external_input = not self.__external_input
        self._conn.write("extin:{}\n".format(self.number).encode('ascii'))

    ###########################################################################

    @property
    def lc_temperature(self):
        """
        Query current temperature of temperature controlled LC on channel n.
        """
        self._conn.write(f"tmp:{self.number},?\n")
        temp = self._conn.readline()
        return (int(temp)*500/65535) - 273.15

    ###########################################################################

    @property
    def temperature_setpoint(self):
        self._conn.write(f"tsp:{self.number},?\n")
        temp = self._conn.readline()
        return (int(temp)*500/65535) - 273.15

    @temperature_setpoint.setter
    def temperature_setpoint(self, value: int):
        value = clamp(value, 0, 65535)
        value = (value + 273.15) * 65535/500
        self._conn.write(f"tsp:{self.number},{value}\n")

    ###########################################################################

    def update_device(self):
        w = self.dict_waveform[self.__waveform]
        n = self.number
        v1 = self.__v1
        v2 = self.__v2
        t = self.__period_t
        ph = self.__phase
        dc = self.__duty_cycle
        tv = self.__tne_voltage
        tt = self.__tne_time

        # TODO: Check if the device ignores the unused parameters.
        message = self.command_waveform[self.__waveform].format(
            w, n, v1, v2, t, ph, dc, tv, tt)
        self._conn.write(message.encode("ascii"))

    def sync(self, phase, pulse_length):
        """
        Produces sync pulse (high-low) on front panel I/O connector of the
        channel, with this phase, and this length

        Parameters
        ----------
        phase : int
            phase relative to waveform (degrees)
        pulse_length: int
            pulse length in microseconds
        """
        self._conn.write(f"sync:{self.number},{phase},{pulse_length}\n")

    @property
    def firmware(self):
        self._conn.write("ver:?\n")
        return self._conn.readline()
