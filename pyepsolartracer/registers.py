# -*- coding: iso-8859-15 -*-
#
# From the PDF

#---------------------------------------------------------------------------#
# Logging
#---------------------------------------------------------------------------#
import logging
_logger = logging.getLogger(__name__)

def V():
    return [ 'Voltage', 'V' ]
def A():
    return [ 'Ampere', 'A' ]
def AH():
    return [ 'Ampere hours', 'Ah' ]
def W():
    return [ 'Watt', 'W' ]
def C():
    return [ 'degree Celsius', '�C' ] # \0xb0
def PC():
    return [ '%, percentage', '%' ]
def KWH():
    return [ 'kWh, kiloWatt/hour', 'kWh' ]
def Ton():
    return [ '1000kg', 't' ]
def MO():
    return [ 'milliohm', 'mOhm' ]
def I():
    return [ 'integer', '' ]
def SEC():
    return [ 'seconds', 's' ]
def MIN():
    return [ 'minutes', 'min' ]
def HOUR():
    return [ 'hours', 'h' ]

class Value:
    '''Value with unit'''
    def __init__(self, register, value):
        self.register = register
        if self.register.times != 1 and value is not None:
            self.value = 1.0 * value / self.register.times
        else:
            self.value = value

    def __str__(self):
        if self.value is None:
            return self.register.name + " = " + str(self.value) 
        return self.register.name + " = " + str(self.value) + self.register.unit()[1]

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

class Register:
    def __init__(self, name, address, description, unit, times, size = 1):
        self.name = name
        self.address = address
        self.description = description
        self.unit = unit
        self.times = times
        self.size = size

    def is_coil(self):
        return self.address < 0x1000

    def is_discrete_input(self):
        return self.address >= 0x1000 and self.address < 0x3000

    def is_input_register(self):
        return self.address >= 0x3000 and self.address < 0x9000

    def is_holding_register(self):
        return self.address >= 0x9000

    def decode(self, response):
        if hasattr(response, "getRegister"):
            mask = rawvalue = lastvalue = 0
            for i in range(self.size):
                lastvalue = response.getRegister(i)
                rawvalue = rawvalue | (lastvalue << (i * 16))
                mask = (mask << 16) | 0xffff
            if (lastvalue & 0x8000) == 0x8000:
                #print rawvalue
                rawvalue = -(rawvalue ^ mask) - 1
            return Value(self, rawvalue)
        _logger.info ("No value for register " + repr(self.name))
        return Value(self, None)

    def encode(self, value):
        # FIXME handle 2 word registers
        rawvalue = int(value * self.times)
        if rawvalue < 0:
            rawvalue = (-rawvalue - 1) ^ 0xffff
            #print rawvalue
        return rawvalue

    def __str__(self):
        return str({ 'address': self.address, 'name': self.name})

class Coil(Register):
    def decode(self, response):
        if hasattr(response, "bits"):
            return Value(self, response.bits[0])
        _logger.info ("No value for coil " + repr(self.name))
        return Value(self, None)

# LS-B Series Protocol
# ModBus Register Address List
# Beijing Epsolar Technology Co., Ltd.
# Notes :
# (1)The ID of the controller is 1 by default and can be modified by PC software(Solar Station Monitor) or
# remote meter MT50.
# (2)The serial communication parameters: 115200bps baudrate, 8 data bits, 1 stop bit and no parity,no
# handshaking.
# (3)The register address below is in hexadecimal format.
# (4)For the data with the length of 32 bits, such as power, using the L and H registers represent the low and
# high 16 bits value,respectively. e.g.The charging input rated power is actually 3000W, multiples of 100 times,
# then the value of 0x3002 register is 0x93E0 and value of 0x3003 is 0x0004

# V1.1
#Variable name, Address, Description, Unit, Times

# Rated data (read only) input register
registers = [
# Charging equipment rated input voltage
Register("Charging equipment rated input voltage",
  0x3000, "PV array rated voltage",
  V, 100 ),
# Charging equipment rated input current
Register("Charging equipment rated input current",
  0x3001, "PV array rated current",
  A, 100 ),
# Charging equipment rated input power
Register("Charging equipment rated input power",
  0x3002, "PV array rated power",
  W, 100, 2),
# Charging equipment rated input power L
Register("Charging equipment rated input power L",
  0x3002, "PV array rated power (low 16 bits)",
  W, 100 ),
# Charging equipment rated input power H
Register("Charging equipment rated input power H",
  0x3003, "PV array rated power (high 16 bits)",
  W, 100 ),
# Charging equipment rated output voltage
Register("Charging equipment rated output voltage",
  0x3004,"Battery's voltage",
  V, 100 ),
# Charging equipment rated output current
Register("Charging equipment rated output current",
  0x3005, "Rated charging current to battery",
  A, 100 ),
# Charging equipment rated output power
Register("Charging equipment rated output power",
  0x3006, "Rated charging power to battery",
  W, 100, 2),
# Charging equipment rated output power L
Register("Charging equipment rated output power L",
  0x3006, "Rated charging power to battery H",
  W, 100 ),
# Charging equipment rated output power H
Register("Charging equipment rated output power H",
  0x3007, "Charging equipment rated output power H",
  W, 100 ),
# Charging mode
Register("Charging mode",
  0x3008, "0001H-PWM",
  I, 1 ),
# Rated output current of load
Register("Rated output current of load",
  0x300E, "Rated output current of load",
  A, 100 ),

# Real-time data (read only) input register
# Charging equipment input voltage
Register("Charging equipment input voltage",
  0x3100, "Solar charge controller--PV array voltage",
  V, 100 ),
# Charging equipment input current
Register("Charging equipment input current",
  0x3101, "Solar charge controller--PV array current",
  A, 100 ),
# Charging equipment input power
Register("Charging equipment input power",
  0x3102, "Solar charge controller--PV array power",
  W, 100, 2 ),
# Charging equipment input power L
Register("Charging equipment input power L",
  0x3102, "Solar charge controller--PV array power",
  W, 100 ),
# Charging equipment input power H
Register("Charging equipment input power H",
  0x3103, "Charging equipment input power H",
  W, 100 ),
# Charging equipment output voltage
Register("Charging equipment output voltage",
  0x3104, "Battery voltage",
  V, 100 ),
# Charging equipment output current
Register("Charging equipment output current",
 0x3105, "Battery charging current",
  A, 100 ),
# Charging equipment output power
Register("Charging equipment output power",
  0x3106, "Battery charging power",
  W, 100, 2 ),
# Charging equipment output power L
Register("Charging equipment output power L",
  0x3106, "Battery charging power",
  W, 100 ),
# Charging equipment output power H
Register("Charging equipment output power H",
  0x3107, "Charging equipment output power H",
  W, 100 ),
# Discharging equipment output voltage
Register("Discharging equipment output voltage",
  0x310C, "Load voltage",
  V, 100 ),
# Discharging equipment output current
Register("Discharging equipment output current",
  0x310D, "Load current",
  A, 100 ),
# Discharging equipment output power
Register("Discharging equipment output power",
  0x310E, "Load power",
  W, 100, 2 ),
# Discharging equipment output power L
Register("Discharging equipment output power L",
  0x310E, "Load power L",
  W, 100 ),
# Discharging equipment output power H
Register("Discharging equipment output power H",
  0x310F, "Discharging equipment output power H",
  W, 100 ),
# Battery Temperature
Register("Battery Temperature",
  0x3110, "Battery Temperature",
  C, 100 ),
# Temperature inside equipment
Register("Temperature inside equipment",
  0x3111, "Temperature inside case",
  C, 100 ),
# Power components temperature
Register("Power components temperature",
  0x3112, "Heat sink surface temperature of equipments' power components",
  C, 100 ),
# Battery SOC
Register("Battery SOC",
  0x311A, "The percentage of battery's remaining capacity",
  PC, 1 ),
# Remote battery temperature
Register("Remote battery temperature",
  0x311B, "The battery tempeture measured by remote temperature sensor",
  C, 100 ),
# Battery's real rated power
Register("Battery's real rated power",
  0x311D, "Current system rated votlage. 1200, 2400 represent 12V, 24V",
  V, 100 ),

# Real-time status (read-only) input re
# Battery statusgister
Register("Battery status",
  0x3200, "D3-D0: 01H Overvolt , 00H Normal , 02H Under Volt, 03H Low Volt Disconnect, 04H Fault D7-D4: 00H Normal, 01H Over Temp.(Higher than the warning settings), 02H Low Temp.( Lower than the warning settings), D8: Battery inerternal resistance abnormal 1, normal 0 D15: 1-Wrong identification for rated voltage",
  I, 1 ),
# Charging equipment status
Register("Charging equipment status",
  0x3201,
"D15-D14: Input volt status. 00 normal, 01 no power connected, 02H Higher volt input, 03H Input volt error. D13: Charging MOSFET is short. D12: Charging or Anti-reverse MOSFET is short. D11: Anti-reverse MOSFET is short. D10: Input is over current. D9: The load is Over current. D8: The load is short. D7: Load MOSFET is short. D4: PV Input is short. D3-2: Charging status. 00 No charging,01 Float,02 Boost,03 Equlization. D1: 0 Normal, 1 Fault. D0: 1 Running, 0 Standby.",
  I, 1),

# Statistical parameter (read only) input register

# Maximum input volt (PV) today
Register("Maximum input volt (PV) today",
  0x3300, "00: 00 Refresh every day",
  V, 100 ),
# Minimum input volt (PV) today
Register("Minimum input volt (PV) today",
  0x3301, "00: 00 Refresh every day",
  V, 100 ),
# Maximum battery volt today
Register("Maximum battery volt today",
  0x3302, "00: 00 Refresh every day",
  V, 100 ),
# Minimum battery volt today
Register("Minimum battery volt today",
  0x3303, "00: 00 Refresh every day",
  V, 100 ),
# Consumed energy today
Register("Consumed energy today",
  0x3304, "00: 00 Clear every day",
  KWH, 100, 2 ),
# Consumed energy today L
Register("Consumed energy today L",
  0x3304, "00: 00 Clear every day",
  KWH, 100 ),
# Consumed energy today H
Register("Consumed energy today H",
  0x3305, "Consumed energy today H",
  KWH, 100 ),
# Consumed energy this month
Register("Consumed energy this month",
  0x3306, "00: 00 Clear on the first day of month",
  KWH, 100, 2 ),
# Consumed energy this month L
Register("Consumed energy this month L",
  0x3306, "00: 00 Clear on the first day of month",
  KWH, 100 ),
# Consumed energy this month H
Register("Consumed energy this month H",
  0x3307, "Consumed energy this month H",
  KWH, 100 ),
# Consumed energy this year
Register("Consumed energy this year",
  0x3308, "00: 00 Clear on 1, Jan.",
  KWH, 100, 2 ),
# Consumed energy this year L
Register("Consumed energy this year L",
  0x3308, "00: 00 Clear on 1, Jan.",
  KWH, 100 ),
# Consumed energy this year H
Register("Consumed energy this year H",
  0x3309, "Consumed energy this year H",
  KWH, 100 ),
# Total consumed energy
Register("Total consumed energy",
  0x330A, "Total consumed energy",
  KWH, 100, 2 ),
# Total consumed energy L
Register("Total consumed energy L",
  0x330A, "Total consumed energy L",
  KWH, 100 ),
# Total consumed energy H
Register("Total consumed energy H",
  0x330B, "Total consumed energy H",
  KWH, 100 ),
# Generated energy today
Register("Generated energy today",
  0x330C, "00: 00 Clear every day.",
  KWH, 100, 2 ),
# Generated energy today L
Register("Generated energy today L",
  0x330C, "00: 00 Clear every day.",
  KWH, 100 ),
# Generated energy today H
Register("Generated energy today H",
  0x330D, "Generated energy today H",
  KWH, 100 ),
# Generated energy this month
Register("Generated energy this month",
  0x330E, "00: 00 Clear on the first day of month.",
  KWH, 100, 2 ),
# Generated energy this month L
Register("Generated energy this month L",
  0x330E, "00: 00 Clear on the first day of month.",
  KWH, 100 ),
# Generated energy this month H
Register("Generated energy this month H",
  0x330F, "Generated energy this month H",
  KWH, 100 ),
# Generated energy this year
Register("Generated energy this year",
  0x3310, "00: 00 Clear on 1, Jan.",
  KWH, 100, 2 ),
# Generated energy this year L
Register("Generated energy this year L",
  0x3310, "00: 00 Clear on 1, Jan.",
  KWH, 100 ),
# Generated energy this year H
Register("Generated energy this year H",
  0x3311, "Generated energy this year H",
  KWH, 100 ),
# Total generated energy
Register("Total generated energy",
  0x3312, "Total generated energy",
  KWH, 100, 2 ),
# Total generated energy L
Register("Total generated energy L",
  0x3312, "Total generated energy L",
  KWH, 100 ),
# Total Generated energy H
Register("Total Generated energy H",
  0x3313, "Total Generated energy H",
  KWH, 100 ),
# Carbon dioxide reduction
Register("Carbon dioxide reduction",
  0x3314, "Saving 1 Kilowatt=Reduction 0.997KG''Carbon dioxide ''=Reduction 0.272KG''Carton''",
  Ton, 100, 2 ),
# Carbon dioxide reduction L
Register("Carbon dioxide reduction L",
  0x3314, "Saving 1 Kilowatt=Reduction 0.997KG''Carbon dioxide ''=Reduction 0.272KG''Carton''",
  Ton, 100 ),
# Carbon dioxide reduction H
Register("Carbon dioxide reduction H",
  0x3315, "Carbon dioxide reduction H",
  Ton, 100 ),
# Battery Current
Register("Battery Current",
  0x331B, "The net battery current,charging current minus the discharging one. The positive value represents charging and negative, discharging.",
  A, 100, 2 ),
# Battery Current L
Register("Battery Current L",
  0x331B, "The net battery current,charging current minus the discharging one. The positive value represents charging and negative, discharging.",
  A, 100 ),
# Battery Current H
Register("Battery Current H",
  0x331C, "Battery Current H",
  A, 100 ),
# Battery Temp.
Register("Battery Temp.",
  0x331D, "Battery Temp.",
  C, 100 ),
# Ambient Temp.
Register("Ambient Temp.",
  0x331E, "Ambient Temp.",
  C, 100 ),

# Setting Parameter (read-write) holding register
# Battery Type
Register("Battery Type",
  0x9000, "0001H- Sealed , 0002H- GEL, 0003H- Flooded, 0000H- User defined",
  I, 1 ),
# Battery Capacity
Register("Battery Capacity",
  0x9001, "Rated capacity of the battery",
  AH, 1 ),
# Temperature compensation coefficient
Register("Temperature compensation coefficient",
  0x9002, "Range 0-9 mV/�C/2V",
  I, 100 ),
# High Volt.disconnect
Register("High Volt.disconnect",
  0x9003, "High Volt.disconnect",
  V, 100 ),
# Charging limit voltage
Register("Charging limit voltage",
  0x9004, "Charging limit voltage",
  V, 100 ),
# Over voltage reconnect
Register("Over voltage reconnect",
  0x9005, "Over voltage reconnect",
  V, 100 ),
# Equalization voltage
Register("Equalization voltage",
  0x9006, "Equalization voltage",
  V, 100 ),
# Boost voltage
Register("Boost voltage",
  0x9007, "Boost voltage",
  V, 100 ),
# Float voltage
Register("Float voltage",
  0x9008, "Float voltage",
  V, 100 ),
# Boost reconnect voltage
Register("Boost reconnect voltage",
  0x9009, "Boost reconnect voltage",
  V, 100 ),
# Low voltage reconnect
Register("Low voltage reconnect",
  0x900A, "Low voltage reconnect",
  V, 100 ),
# Under voltage recover
Register("Under voltage recover",
  0x900B, "Under voltage recover",
  V, 100 ),
# Under voltage warning
Register("Under voltage warning",
  0x900C, "Under voltage warning",
  V, 100 ),
# Low voltage disconnect
Register("Low voltage disconnect",
  0x900D, "Low voltage disconnect",
  V, 100 ),
# Discharging limit voltage
Register("Discharging limit voltage",
  0x900E, "Discharging limit voltage",
  V, 100 ),
# Real time clock 1
Register("Real time clock 1",
  0x9013, "D7-0 Sec, D15-8 Min.(Year,Month,Day,Min,Sec.should be writed simultaneously)",
  I, 1 ),
# Real time clock 2
Register("Real time clock 2",
  0x9014, "D7-0 Hour, D15-8 Day",
  I, 1 ),
# Real time clock 3
Register("Real time clock 3",
  0x9015, "D7-0 Month, D15-8 Year",
  I, 1 ),
# Equalization charging cycle
Register("Equalization charging cycle",
  0x9016, "Interval days of auto equalization charging in cycle Day",
  I, 1 ),
# Battery temperature warning upper limit
Register("Battery temperature warning upper limit",
  0x9017, "Battery temperature warning upper limit",
  C, 100 ),
# Battery temperature warning lower limit
Register("Battery temperature warning lower limit",
  0x9018, "Battery temperature warning lower limit",
  C, 100 ),
# Controller inner temperature upper limit
Register("Controller inner temperature upper limit",
  0x9019, "Controller inner temperature upper limit",
  C, 100 ),
# Controller inner temperature upper limit recover
Register("Controller inner temperature upper limit recover",
  0x901A, "After Over Temperature, system recover once it drop to lower than this value",
  C, 100 ),
# Power component temperature upper limit
Register("Power component temperature upper limit",
  0x901B, "Warning when surface temperature of power components higher than this value, and charging and discharging stop",
  C, 100 ),
# Power component temperature upper limit recover
Register("Power component temperature upper limit recover",
  0x901C, "Recover once power components temperature lower than this value",
  C, 100 ),
# Line Impedance
Register("Line Impedance",
  0x901D, "The resistance of the connectted wires.",
  MO, 100 ),
# Night TimeThreshold Volt.(NTTV)
Register("Night TimeThreshold Volt.(NTTV)",
  0x901E, " PV lower lower than this value, controller would detect it as sundown",
  V, 100 ),
# Light signal startup (night) delay time
Register("Light signal startup (night) delay time",
  0x901F, "PV voltage lower than NTTV, and duration exceeds the Light signal startup (night) delay time, controller would detect it as night time.",
  MIN, 1 ),
# Day Time Threshold Volt.(DTTV)
Register("Day Time Threshold Volt.(DTTV)",
  0x9020, "PV voltage higher than this value, controller would detect it as sunrise",
  V, 100 ),
# Light signal turn off(day) delay time
Register("Light signal turn off(day) delay time",
  0x9021, "PV voltage higher than DTTV, and duration exceeds Light signal turn off(day) delay time delay time, controller would detect it as daytime.",
  MIN, 1 ),
# Load controling modes
Register("Load controling modes",
  0x903D,"0000H Manual Control, 0001H Light ON/OFF, 0002H Light ON+ Timer/, 0003H Time Control",
  I, 1 ),
# Working time length 1
Register("Working time length 1",
  0x903E, "The length of load output timer1, D15-D8,hour, D7-D0, minute",
  I, 1 ),
# Working time length 2
Register("Working time length 2",
  0x903F, "The length of load output timer2, D15-D8, hour, D7-D0, minute",
  I, 1 ),
# Turn on timing 1 sec
Register("Turn on timing 1 sec",
  0x9042, "Turn on timing 1 sec",
  SEC, 1),
# Turn on timing 1 min
Register("Turn on timing 1 min",
  0x9043, "Turn on timing 1 min",
  MIN, 1),
# Turn on timing 1 hour
Register("Turn on timing 1 hour",
  0x9044, "Turn on timing 1 hour",
  HOUR, 1),
# Turn off timing 1 sec
Register("Turn off timing 1 sec",
  0x9045, "Turn off timing 1 sec",
  SEC, 1),
# Turn off timing 1 min
Register("Turn off timing 1 min",
  0x9046, "Turn off timing 1 min",
  MIN, 1 ),
# Turn off timing  hour
Register("Turn off timing 1 hour",
  0x9047, "Turn off timing 1 hour",
  HOUR, 1 ),
# Turn on timing 2 sec
Register("Turn on timing 2 sec",
  0x9048, "Turn on timing 2 sec",
  SEC, 1 ),
# Turn on timing 2 min
Register("Turn on timing 2 min",
  0x9049, "Turn on timing 2 min",
  MIN, 1 ),
# Turn on timing 2 hour
Register("Turn on timing 2 hour",
  0x904A, "Turn on timing 2 hour",
  HOUR, 1 ),
# Turn off timing 2 sec
Register("Turn off timing 2 sec",
  0x904B, "Turn off timing 2 sec",
  SEC, 1 ),
# Turn off timing 2 min
Register("Turn off timing 2 min",
  0x904C, "Turn off timing 2 min",
  MIN, 1 ),
# Turn off timing 2 hour
Register("Turn off timing 2 hour",
  0x904D, "Turn off timing 2 hour",
  HOUR, 1),
# Length of night
Register("Length of night",
  0x9065, "Set default values of the whole night length of time. D15-D8,hour, D7-D0, minute",
  I, 1 ),
# Battery rated voltage code
Register("Battery rated voltage code",
  0x9067, "0, auto recognize. 1-12V, 2-24V",
  I, 1 ),
# Load timing control selection
Register("Load timing control selection",
  0x9069, "Selected timeing period of the load.0, using one timer, 1-using two timer, likewise.",
  I, 1 ),
# Default Load On/Off in manual mode
Register("Default Load On/Off in manual mode",
  0x906A, "0-off, 1-on",
  I, 1 ),
# Equalize duration
Register("Equalize duration",
  0x906B, "Usually 60-120 minutes.",
  MIN, 1 ),
# Boost duration
Register("Boost duration",
  0x906C, "Usually 60-120 minutes.",
  MIN, 1 ),
# Discharging percentage
Register("Discharging percentage",
  0x906D, "Usually 20%-80%. The percentage of battery's remaining capacity when stop charging",
  PC, 1 ),
# Charging percentage
Register("Charging percentage",
  0x906E, "Depth of charge, 20%-100%.",
  PC, 1 ),
#906f?
# Management modes of battery charging and discharging
Register("Management modes of battery charging and discharging",
  0x9070, "Management modes of battery charge and discharge, voltage compensation : 0 and SOC : 1.",
  I, 1 ),
];

coils = [
# Coils(read-write)
# Manual control the load
Coil("Manual control the load",
  2,  "When the load is manual mode, 1-manual on, 0 -manual off",
  I, 1 ),
# Enable load test mode
Coil("Enable load test mode",
  5, "1 Enable, 0 Disable(normal)",
  I, 1 ),
# Force the load on/off
Coil("Force the load on/off",
  6, "1 Turn on, 0 Turn off (used for temporary test of the load)",
  I, 1 ),

# Discrete input (read-only)
# Over temperature inside the device
Coil("Over temperature inside the device",
  0x2000, "1 The temperature inside the controller is higher than the over-temperature protection point. 0 Normal",
  I, 1 ),
# Day/Night
Coil("Day/Night",
  0x200C, "1-Night, 0-Day",
  I, 1 ),
];

# RJ45 pinout
#1, 2- No connected
#3, 4- RS-485 A
#5, 6- RS-485 B
#7, 8- Ground
# The pins define for the RJ-45 port of LS-B controller. Pin 3 and 4 is the A of RS-485, Pin 5 and 6 is B.
#
# (1) To improve the communication quality, the ground pins 7 and 8 (connected with the negative terminal of
# the battery) could be used if necessary. However, the user must care the common ground problem of the
# connected devices.
# (2) User is advised to do not use the pin 1 and pin 2 for the device's safety

_registerByName = {}

for reg in registers:
    name = reg.name
    if name in _registerByName:
        raise Exception("internal error " + name)
    _registerByName[name] = reg

for reg in coils:
    name = reg.name
    if name in _registerByName:
        raise Exception("internal error " + name)
    _registerByName[name] = reg

def registerByName(name):
    if name not in _registerByName:
        raise Exception("Unknown register "+repr(name))
    return _registerByName[name]
    
__all__ = [
    "registers",
    "coils",
    "registerByName",
]
