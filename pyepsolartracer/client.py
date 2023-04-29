# -*- coding: iso-8859-15 -*-

# import the server implementation
from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.mei_message import *
from pymodbus.exceptions import ParameterException
from pyepsolartracer.registers import registerByName
from datetime import datetime

#---------------------------------------------------------------------------#
# Logging
#---------------------------------------------------------------------------#
import logging
_logger = logging.getLogger(__name__)

class EPsolarTracerClient:
    ''' EPsolar Tracer client
    '''

    def __init__(self, unit = 1, serialclient = None, **kwargs):
        ''' Initialize a serial client instance
        '''
        self.unit = unit
        if serialclient == None:
            port = kwargs.get('port', '/dev/ttyXRUSB0')
            baudrate = kwargs.get('baudrate', 115200)
            self.client = ModbusClient(method = 'rtu', port = port, baudrate = baudrate, kwargs = kwargs)
        else:
            self.client = serialclient

    def connect(self):
        ''' Connect to the serial
        :returns: True if connection succeeded, False otherwise
        '''
        return self.client.connect()

    def close(self):
        ''' Closes the underlying connection
        '''
        return self.client.close()

    def read_device_info(self):
        request = ReadDeviceInformationRequest (unit = self.unit)
        response = self.client.execute(request)
        if response.isError():
            raise response
        return response

    def read_input(self, name):
        register = registerByName(name)
        if register.is_coil():
            response = self.client.read_coils(address=register.address, count=register.size, slave = self.unit)
            _logger.debug("Read holding coil '%s' : %s", name, response)
        elif register.is_discrete_input():
            response = self.client.read_discrete_inputs(address=register.address, count=register.size, slave = self.unit)
            _logger.debug("Read discrete input '%s' : %s", name, response)
        elif register.is_input_register():
            response = self.client.read_input_registers(address=register.address, count=register.size, slave = self.unit)
            _logger.debug("Read input register '%s' : %s", name, response)
        else:
            response = self.client.read_holding_registers(address=register.address, count=register.size, slave = self.unit)
            _logger.debug("Read holding register '%s' : %s", name, response)
        if response.isError():
            raise response
        return register.decode(response)

    def write_output(self, name, value):
        register = registerByName(name)
        values = register.encode(value)
        response = False
        if register.is_coil():
            _logger.debug("Write coil '%s' : %s", name, value)
            response = self.client.write_coil(address=register.address, value=values, slave = self.unit)
        elif register.is_discrete_input():
            _logger.error("Cannot write discrete input '%s'", name)
            raise ParameterException("Cannot write discrete input: " + repr(name))
            pass
        elif register.is_input_register():
            _logger.error("Cannot write input register '%s' " , name)
            raise ParameterException("Cannot write input register: " + repr(name))
            pass
        else:
            _logger.debug("Write register %s : %s", name, value)
            response = self.client.write_registers(address=register.address, value=values, slave = self.unit)
        if response.isError():
            raise response
        return response

    def readRTC(self):
        register = registerByName('Real time clock 1')
        sizeAddress = 3
        result = self.client.read_holding_registers(register.address, sizeAddress, slave = self.unit)
        if result.isError():
            raise result
        return self.decodeRTC(result.registers)

    def writeRTC(self, datetime):
        register = registerByName('Real time clock 1')
        values = self.encodeRTC(datetime)
        result = self.client.write_registers(register.address, values, slave = self.unit)
        if result.isError():
            raise result
        return True

    def decodeRTC(self, rtc):
        s = 2000
        secMin  = rtc[0]
        hourDay = rtc[1]
        monthYear = rtc[2]
        secs  = (secMin & 0xff)
        hour  = (hourDay & 0xff)
        month = (monthYear & 0xff)
        minut = secMin    >> 8
        day   = hourDay   >> 8
        year  = monthYear >> 8
        return datetime(s+year, month, day, hour, minut, secs)

    def encodeRTC(self, datetime):
        s = 2000
        rtc1 = int( (datetime.minute  << 8) | datetime.second)
        rtc2 = int( (datetime.day 	  << 8) | datetime.hour)
        rtc3 = int( (datetime.year -s << 8) | datetime.month)
        return [rtc1, rtc2, rtc3]

__all__ = [
    "EPsolarTracerClient",
]
