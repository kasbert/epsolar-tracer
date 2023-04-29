#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-


# Read info with ModbusClient

import time

# import the server implementation
from pymodbus.client import ModbusSerialClient as ModbusClient
#from test.testdata import ModbusMockClient as ModbusClient
from pymodbus.mei_message import *
from pyepsolartracer.registers import registers,coils
import serial.rs485

# configure the client logging
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# choose the serial client
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=115200, stopbits = 1, bytesize = 8, timeout=1)
client.connect()
try:
    client.socket.rs485_mode = serial.rs485.RS485Settings()
except:
    pass

request = ReadDeviceInformationRequest(unit=1)
response = client.execute(request)

if hasattr(response, 'information'):
    print ('ReadDeviceInformationRequest', repr(response.information))
else:
    print ('ReadDeviceInformationRequest', repr(response))

unit = 1

for reg in registers:
    print()
    print(reg, reg.is_input_register(), reg.is_holding_register())
    if reg.is_input_register():
        rr = client.read_input_registers(address=reg.address, count=reg.size, slave = unit)
        print("read_input_registers:", rr.getRegister(0))
    else:
        rr = client.read_holding_registers(address=reg.address, count=reg.size, slave = unit)
        print("read_holding_registers:", rr.getRegister(0))
    value = reg.decode(rr)
    print (rr, value)

for reg in coils:
    print()
    print(reg, reg.is_coil(), reg.is_discrete_input())
    if reg.is_coil():
        rr = client.read_coils(address = reg.address, count = reg.size, slave = unit)
        if hasattr(rr, "bits"):
            print("read_coils:", str(rr.bits))
        else:
            print("read_coils:", str(rr))
    elif reg.is_discrete_input():
        rr = client.read_discrete_inputs(address = reg.address, count = reg.size, slave = unit)
        if hasattr(rr, "bits"):
            print("read_discrete_inputs:", str(rr.bits))
        else:
            print("read_discrete_inputs:", str(rr))
    value = reg.decode(rr)
    print (rr, value)
