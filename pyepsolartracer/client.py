# -*- coding: iso-8859-15 -*-

# import the server implementation
from pymodbus.client import ModbusSerialClient as ModbusClient
#from pymodbus.mei_message import *
from pymodbus.mei_message import ReadDeviceInformationRequest
from pymodbus.exceptions import ParameterException, ModbusException
from pymodbus.pdu import ExceptionResponse
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
        if isinstance(response, ModbusException):
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
            _logger.debug("Read input register '%s' : %s", name, register.rawvalue(response))
        else:
            response = self.client.read_holding_registers(address=register.address, count=register.size, slave = self.unit)
            _logger.debug("Read holding register '%s' : %s", name, register.rawvalue(response))
        if isinstance(response, ModbusException):
            raise response
        return register.decode(response)

    def write_output(self, name, value):
        register = registerByName(name)
        values = register.encode(value)
        response = False
        if register.is_coil():
            _logger.debug("Write coil '%s' : %s", name, values)
            response = self.client.write_coil(address=register.address, value=values, slave = self.unit)
        elif register.is_discrete_input():
            _logger.error("Cannot write discrete input '%s'", name)
            raise ParameterException("Cannot write discrete input: " + repr(name))
        elif register.is_input_register():
            _logger.error("Cannot write input register '%s' " , name)
            raise ParameterException("Cannot write input register: " + repr(name))
        else:
            _logger.debug("Write register '%s' : %s", name, values)
            if register.size == 1:
                response = self.client.write_register(address=register.address, value=values, slave = self.unit)
            else:
                response = self.client.write_registers(address=register.address, values=values, slave = self.unit)
        if isinstance(response, ExceptionResponse):
            raise ModbusException(str(response))
        if isinstance(response, ModbusException):
            print(repr(response))
            print(response)
            raise response
        return response

    def readRTC(self):
        result = self.read_input('Real time clock')
        return self.decodeRTC(result.value)

    def writeRTC(self, dtime):
        values = self.encodeRTC(dtime)
        self.write_output('Real time clock', values)
        return True

    def decodeRTC(self, rtc):
        secs = (rtc >> 0) & 0xff
        minut = (rtc >> 8) & 0xff
        hour = (rtc >> 16) & 0xff
        day = (rtc >> 24) & 0xff
        month = (rtc >> 32) & 0xff
        year = (rtc >> 40) & 0xff
        s = 2000
        return datetime(s+year, month, day, hour, minut, secs)

    def encodeRTC(self, datetime):
        s = 2000
        return (datetime.second << 0) | (datetime.minute << 8) | (datetime.hour << 16) | (datetime.day << 24) | (datetime.month << 32) | ((datetime.year - s) << 40)

__all__ = [
    "EPsolarTracerClient",
]
