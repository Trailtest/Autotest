#!/usr/bin/env python
import sys
from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

INA_Module = [[0x40, "External Input"], [0x41, "Internal Battery"], [
    0x44, "PoE Input"], [0x45, "PoE Output"]]


class InaControl:

    def read(self, device):
        address = device[0]
        monitoredDevice = device[1]

        print "**********%s*********" % monitoredDevice
        print "Device Addres: %x" % address

        ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address)
        ina.configure()

        print "Bus Voltage: %.3f V" % ina.voltage()
        try:
            current = ina.current()
            print "Bus Current: %.3f mA" % current
            print "Power: %.3f mW" % ina.power()
            if current < 0:
                print "State: Charging\n"
            elif current > 0:
                if address == 0x44:
                    print "Power Supplied to GBC via PoE"
                elif address == 0x45:
                    print "Power delivered to Load via PoE"
                else:
                    print "State: Discharging\n"
        except DeviceRangeError as e:
            # Current out of device range with specified shunt resister
            print e

    def processRead(self, userVal):

        if userVal == 0:
            self.read(INA_Module[0])
        elif userVal == 1:
            self.read(INA_Module[1])
        elif userVal == 2:
            self.read(INA_Module[2])
        elif userVal == 3:
            self.read(INA_Module[3])
        elif userVal == 4:
            for listVal in INA_Module:
                self.read(listVal)
        else:
            print('invalid option')


g = InaControl()
g.processRead(int(sys.argv[1]))
