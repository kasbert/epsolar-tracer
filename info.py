
from pyepsolartracer.client import EPsolarTracerClient
from pyepsolartracer.registers import registers,coils
from test.testdata import ModbusMockClient as ModbusClient

# configure the client logging
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

serialclient = ModbusClient()
#serialclient = None

client = EPsolarTracerClient(serialclient = serialclient)
client.connect()

response = client.read_device_info()
print "Manufacturer:", repr(response.information[0])
print "Model:", repr(response.information[1])
print "Version:", repr(response.information[2])

response = client.read_input("Charging equipment rated input voltage")
print str(response)

for reg in registers:
    #print
    #print reg
    value = client.read_input(reg.name)
    print value
    #if value.value is not None:
    #    print client.write_output(reg.name,value.value)

for reg in coils:
    #print
    #print reg
    value = client.read_input(reg.name)
    print value
    #print client.write_output(reg.name,value.value)

client.close()
