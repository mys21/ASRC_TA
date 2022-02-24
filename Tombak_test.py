import numpy as np
import serial


ser = serial.Serial('COM3')  # open serial port
print(ser.name)         # check which port was really used
ser.baudrate = 125000
print(ser)
cmd = ('$04$00$01$03').encode('UTF-8')
ser.write(cmd)   # write a string
print(ser.read(100).decode('ascii'))
ser.close() 
