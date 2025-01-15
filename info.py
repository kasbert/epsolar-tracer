#!/usr/bin/env python3

from pyepsolartracer.client import EPsolarTracerClient
from pyepsolartracer.registers import registers,coils
from pymodbus.client import ModbusSerialClient as ModbusClient
#from test.testdata import ModbusMockClient as ModbusClient
from datetime import datetime
import time
import serial.rs485

# configure the client logging
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)
#log.setLevel(logging.DEBUG)

# choose the serial client
serialclient = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=115200, stopbits = 1, bytesize = 8, timeout=1)
serialclient.connect()
try:
    serialclient.socket.rs485_mode = serial.rs485.RS485Settings(rts_level_for_rx=True,rts_level_for_tx=False)
except:
    pass

client = EPsolarTracerClient(serialclient = serialclient)

response = client.read_device_info()
print("Manufacturer:", repr(response.information[0]))
print("Model:", repr(response.information[1]))
print("Version:", repr(response.information[2]))

response = client.read_input("Charging equipment rated input voltage")
print(str(response))

response = client.readRTC()
print("readRTC", str(response))
response = client.writeRTC(datetime.now())
print("writeRTC", str(response))
#response = client.writeRTC(datetime(2023,1,2,3,4,5))
#print("writeRTC", str(response))
response = client.readRTC()
print("readRTC", str(response))

#print (client.read_input("Battery temperature warning upper limit"))
#client.write_output("Battery temperature warning upper limit", 65.0)
#print (client.read_input("Battery temperature warning upper limit"))

#print (client.read_input('Battery Type'))
#client.write_output('Battery Type', 0)
#time.sleep(0.5)
print (client.read_input('Battery Type'))

time.sleep(0.5)
print (client.read_input("High Volt.disconnect"))
#time.sleep(0.5)
#client.write_output("High Volt.disconnect", 16.0)
#time.sleep(0.5)
#print (client.read_input("High Volt.disconnect"))

#client.write_output("Battery rated voltage code", 0)

print (client.read_input("Load controling modes"))
client.write_output("Load controling modes", 0)
print (client.read_input("Load controling modes"))
#print ("Power off")
#client.write_output("Manual control the load", 0)
time.sleep(2)
print ("Power on")
client.write_output("Manual control the load", 1)

response = client.readRTC()
print("readRTC", str(response))

for reg in registers:
    #print()
    #print(reg)
    value = client.read_input(reg.name)
    print(value)
    #if value.value is not None:
    #    print(client.write_output(reg.name,value.value))

for reg in coils:
    #print()
    #print(reg)
    value = client.read_input(reg.name)
    print(value)
    #print(client.write_output(reg.name,value.value))

client.close()
