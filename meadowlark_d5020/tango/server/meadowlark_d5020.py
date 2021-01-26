# -*- coding: utf-8 -*-
#
# This file is part of the Meadowlark D5020 project
#
# Copyright (c) 2021 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more info.

"""Tango server class for Meadowlark_d5020"""

import serial
from tango import GreenMode
from tango.server import Device, attribute, command, device_property

import meadowlark_d5020.core
from meadowlark_d5020.core import Waveform

class Meadowlark_d5020(Device):

    url = device_property(dtype=str)

    def init_device(self):
        super().init_device()
        self.connection = serial.connection_for_url(self.url)
        self.meadowlark_d5020 = meadowlark_d5020.core.Meadowlark_d5020(self.connection)

    ###########################################################################

    @attribute(dtype=Waveform, label="Waveform pattern")
    def waveform(self):
        return self.meadowlark_d5020.waveform

    @waveform.setter
    def set_waveform(self, value):
        self.meadowlark_d5020.waveform = value
    
    ###########################################################################

    @attribute(dtype=int, unit="mV", label="V1", min_value=0, max_value=10000,
               doc="v1")
    def v1(self):        
        return self.meadowlark_d5020.v1

    @v1.setter
    def set_v1(self, value):        
        self.meadowlark_d5020.v1 = value

    ###########################################################################

    @attribute(dtype=int, unit="mV", label="V2", min_value=0, max_value=10000,
               doc="v2")
    def v2(self):        
        return self.meadowlark_d5020.v2

    @v2.setter
    def set_v2(self, value):        
        self.meadowlark_d5020.v2 = value

    ###########################################################################

    @attribute(dtype=int, unit="ms", label="period", min_value=0, max_value=65535,
               doc="period")
    def period(self):        
        return self.meadowlark_d5020.period

    @period.setter
    def set_period(self, value):        
        self.meadowlark_d5020.period = value

    ###########################################################################

    @attribute(dtype=int, unit="degrees", label="phase", min_value=-360, max_value=360,
               doc="phase")
    def phase(self):        
        return self.meadowlark_d5020.phase

    @phase.setter
    def set_phase(self, value):        
        self.meadowlark_d5020.phase = value

    ###########################################################################

    @attribute(dtype=int, unit="%", label="duty cycle", min_value=0, max_value=100,
               doc="duty cycle")
    def duty_cycle(self):        
        return self.meadowlark_d5020.duty_cycle

    @duty_cycle.setter
    def set_duty_cycle(self, value):        
        self.meadowlark_d5020.duty_cycle = value

    ###########################################################################

    @attribute(dtype=int, unit="mV", label="Transient Nematic Effect Voltage", 
               min_value=0, max_value=10000, doc="T.N.E Voltage")
    def tne_voltage(self):        
        return self.meadowlark_d5020.tne_voltage

    @tne_voltage.setter
    def set_tne_voltage(self, value):        
        self.meadowlark_d5020.tne_voltage = value

    ###########################################################################

    @attribute(dtype=bool, label="External input", 
               doc="Check if the external input is enabled")
    def external_input(self):
        return self.meadowlark_d5020.external_input

    @command
    def toggle_external_input(self):        
        self.meadowlark_d5020.toggle_external_input()

    ###########################################################################

    @command
    def turn_on(self):
        # example returning the coroutine back to who calling function
        return self.meadowlark_d5020.turn_on()


if __name__ == "__main__":
    import logging
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level="DEBUG", format=fmt)
    Meadowlark_d5020.run_server()
