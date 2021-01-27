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


class Channels(Enum):
    One = 1
    Two = 2


class Channel:
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

    def __init__(self, number: Channels, conn: Serial):
        # Channel number
        self.number = number.value
        self._conn = conn

        # Default parameters of the Channel
        self.__waveform = Waveform.invariant
        self.__v1 = 0
        self.__v2 = 0
        self.__period_t = 1000
        self.__phase = 0
        self.__duty_cycle = 0
        # Parameters of Transient Nematic Effect
        self.__tne_voltage = 0
        self.__tne_time = 0

        # Others
        self.__external_input = False

        self.dict_waveform = dict(
            invariant="inv", sinusoid="sin", triangle="tri", square="sqr",
            sawtooth="saw", TNE="tnew")

    ###########################################################################

    @property
    def waveform(self):
        return self.__waveform

    @waveform.setter
    def waveform(self, value : Waveform):
        self.__waveform = value

    ###########################################################################

    @property
    def v1(self):
        return self.__v1

    @v1.setter
    def v1(self, value):
        self.__v1 = clamp(value, Channel.MIN_VOLTAGE, Channel.MAX_VOLTAGE)
        self.update_device()

    ###########################################################################

    @property
    def v2(self):
        return self.__v2

    @v2.setter
    def v2(self, value):
        self.__v2 = clamp(value, Channel.MIN_VOLTAGE, Channel.MAX_VOLTAGE)
        self.update_device()
    
    ###########################################################################

    @property
    def period(self):
        return self.__period_t

    @period.setter
    def period(self, value):
        self.__period_t = clamp(value, Channel.MIN_PERIOD, Channel.MAX_PERIOD)
        self.update_device()

    ###########################################################################

    @property
    def phase(self):
        return self.__phase

    @phase.setter
    def phase(self, value):
        self.__phase = value % Channel.MAX_PHASE
        self.update_device()

    ###########################################################################

    @property
    def duty_cycle(self):
        return self.__duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, value):
        self.__duty_cycle = clamp(value, Channel.MIN_DUTY_CICLE, Channel.MAX_DUTY_CICLE)
        self.update_device()

    ###########################################################################

    @property
    def tne_voltage(self):
        return self.__tne_voltage

    @tne_voltage.setter
    def tne_voltage(self, value):
        self.__tne_voltage = clamp(value, Channel.MIN_VOLTAGE, Channel.MAX_VOLTAGE)
        self.update_device()

    ###########################################################################

    @property
    def tne_time(self):
        return self.__tne_time

    @tne_time.setter
    def tne_time(self, value):
        self.__tne_time = clamp(value, Channel.MIN_TNE_TIME, Channel.MAX_TNE_TIME)
        self.update_device()

    ###########################################################################

    @property
    def external_input(self):
        return self.__external_input

    def toggle_external_input(self):
        # TODO: Check if sending this command twice disable the external input.
        self.__external_input = not self.__external_input
        self._conn.write(f"extin:{self.number}\n")

    ###########################################################################

    def threshold(self, V1, V2):
        """
        I/O connector n is monitored, and if less than 2.5V, output = V1. 
        Otherwise, output is V2.
        """
        V1 = clamp(V1, Channel.MIN_VOLTAGE, Channel.MAX_VOLTAGE)
        V2 = clamp(V2, Channel.MIN_VOLTAGE, Channel.MAX_VOLTAGE)
        self._conn.write(f"thr:{self.number},{V1},{V2}\n")

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

    def trigger(self):
        # TODO: Check if sending the command returns somethind, and if sended
        # again disables the trigger.
        """
        I/O connector n is monitored for pulses. When a pulse is received, if 
        the output is at V1, it switches to V2. If the output is at V2, it 
        switches to V1.
        """
        self._conn.write(f"trg:{self.number},?\n")

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
        w = self.dict_waveform[self.__waveform.name]
        n = self.number
        v1 = self.__v1
        v2 = self.__v2
        t = self.__period_t
        ph = self.__phase
        dc = self.__duty_cycle
        tv = self.__vTNE
        tt = self.__tTNE

        # TODO: Check if the device ignores the unused parameters.
        self._conn.write(f"{w}:{n},{v1},{v2},{t},{ph},{dc},{tv},{tt}\n")

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


class Meadowlark_d5020:
    """The central Meadowlark_d5020"""

    def __init__(self, conn):
        self._conn = conn

        self.channel_1 = Channel(Channels.One, conn)
        self.channel_2 = Channel(Channels.Two, conn)

        self.channels = [self.channel_1, self.channel_2]


    @property
    def firmware(self):
        self._conn.write("ver:?\n")
        return self._conn.readline()
