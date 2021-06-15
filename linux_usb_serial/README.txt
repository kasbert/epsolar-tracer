
# xr_serial.c copy from https://raw.githubusercontent.com/torvalds/linux/v5.13-rc6/drivers/usb/serial/xr_serial.c

# Added TIOCGRS485 and TIOCSRS485 ioctls to control RS-485 mode

sudo rmmod cdc-acm
sudo rmmod xr_serial
sudo rmmod xr_usb_serial_common
sudo modprobe -r usbserial
sudo modprobe usbserial
sudo insmod ./xr_serial.ko
