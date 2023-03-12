# epsolar-tracer
Tools for EPsolar Tracer A and BN solar charge controller
===================================================
![Img](img/epsolar_tracer_bn.jpg)

This is the second generation of the EPsolar Tracer solar charge controller. 
You need RS-485 adapter for communication. The first generation controller 
used RS-232 and a different protocol. see https://github.com/xxv/tracer.

[Product link 1](http://www.epsolarpv.com/en/index.php/Product/pro_content/id/573/am_id/136)  
[Product link 2](http://www.epsolarpv.com/en/index.php/Product/index/id/653/am_id/134)  

Check [EPEVER site](https://www.epever.com/) for more info and Windows software.
There are also some [nice pictures](http://gwl-power.tumblr.com/tagged/tracer) on Tumblr.

Linux driver for Exar USB UART
------------------------------
In [directory](xr_usb_serial_common-1a) there is a Linux driver for Exar based USB RS-485 adapter. 
The original source was from Exar website, but it has dissapeared when MaxLinear acquired Exar.

Protocol
--------
[Protocol](archive/1733_modbus_protocol.pdf)
See for [windows capture](archive/epsolar.txt) for some extra commands.

Python module
-------------
Uses modbus library (https://github.com/bashwork/pymodbus)  
Example output
```
# python info.py 
Manufacturer: 'EPsolar Tech co., Ltd'
Model: 'Tracer2215BN'
Version: 'V02.05+V07.12'
Charging equipment rated input voltage = 150.0V
Charging equipment rated input voltage = 150.0V
Charging equipment rated input current = 20.0A
...
```
Wiring
------
Epsolar controller uses RJ45 connector. If you use other RS-485 adapter than Exar, you may create the cable from an Ethernet cable.
Connect orange wire to adapter pin marked as A or D+ and blue wire to the adapter pin marked as B or D-
The other pins are used by MT-50 display and not needed with USB adapter.

| Pin | Function  | Wire  | Eth. Color  	| 
|---	|---        |---	  |---	          |
| 1  	| Ground    |   	  | White-Green   |
| 2  	| Ground    |   	  | Green         |
| 3  	| RS-485-B  |       | White-Orange  |
| 4  	| RS-485-B  | D - 	| Blue          |
| 5  	| RS-485-A  |       | White-Blue    |
| 6  	| RS-485-A  | D +   | Orange  	    |
| 7  	| +7.5V  	  |   	  | White-Brown   |
| 8  	| +7.5V  	  |   	  | Brown	        |

