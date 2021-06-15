#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import time

# import the server implementation
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from test.testdata import ModbusMockClient as ModbusClient
from pymodbus.mei_message import *
from pyepsolartracer.registers import registers,coils
import serial.rs485

# configure the client logging
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# choose the serial client
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=115200, stopbits = 1, bytesize = 8, timeout=1)
client.connect()
rs485_mode = serial.rs485.RS485Settings(delay_before_tx = 0, delay_before_rx = 0, rts_level_for_tx=True, rts_level_for_rx=False, loopback=False)
client.socket.rs485_mode = rs485_mode

request = ReadDeviceInformationRequest(unit=1)
response = client.execute(request)

if hasattr(response, 'information'):
    print (repr(response.information))
else:
    print (repr(response))

for reg in registers:
    print()
    print(reg)
    rr = client.read_input_registers(reg.address, 1, unit=1)
    if hasattr(rr, "getRegister"):
        print("read_input_registers:", rr.getRegister(0))
    else:
        print("read_input_registers", str(rr))
    rr = client.read_holding_registers(reg.address, 1, unit=1)
    if hasattr(rr, "getRegister"):
        print("read_holding_registers:", rr.getRegister(0))
    else:
        print("read_holding_registers:", str(rr))

for reg in coils:
    print()
    print(reg)
    rr =client.read_coils(reg.address, unit=1)
    if hasattr(rr, "bits"):
        print("read_coils:", str(rr.bits))
    else:
        print("read_coils:", str(rr))
    rr = client.read_discrete_inputs(reg.address, unit=1)
    if hasattr(rr, "bits"):
        print("read_discrete_inputs:", str(rr.bits))
    else:
        print("read_discrete_inputs:", str(rr))


