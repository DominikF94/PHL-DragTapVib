import serial
from helpers.usbPorts import gloveUSB


serGlove = serial.Serial(gloveUSB, 9600)
serGlove = serGlove.write(bytes("1,2,3,4,5,5,4,3,2,1,1,2,3,4,5,5,4,3,2,1>", "utf-8)"))