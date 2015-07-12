
from pyepsolartracer.tracer import EPsolarTracerClient

from test.testdata import ModbusMockClient as ModbusClient

serialclient = ModbusClient()
#serialclient = None

client = EPsolarTracerClient(serialclient = serialclient)
client.connect()
response = client.read_device_info()
print "Manufacturer:", repr(response.information[0])
print "Model:", repr(response.information[1])
print "Version:", repr(response.information[2])
client.close()
