from ctypes import *
import os
import numpy as np
from enum import IntEnum
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot	
from time import time, sleep
import datetime
from math import ceil, floor
from Tombak_control import Tombak_control
import pylablib.devices.IMAQ as IMAQ #move to header
import matplotlib.pyplot as plt


img1 = IMAQ.IMAQ.IMAQFrameGrabber(imaq_name='img0')
#img1 = IMAQ.IMAQ.IMAQCamera(name='img0')
img1.open()
img1.set_grabber_attribute_value('IMG_ATTR_ACQWINDOW_HEIGHT',50,'auto')
img1.setup_serial_params('\r','str')
img1.serial_write('OPR 12')
print(img1.serial_readline())
img1.serial_write('TRIG:MODE 1')
print(img1.serial_readline())
img1.serial_write('TRIG:MODE?')
print(img1.serial_readline())
img1.serial_write('EXP?')
print(img1.serial_readline())
img1.serial_write('FRAME:PERIOD?')
print(img1.serial_readline())
img1.serial_write('TRIG:SOURCE?')
print(img1.serial_readline())

print(img1.get_frames_status())
img1.clear_acquisition()
x = datetime.datetime.now()
data = np.array(img1.grab(nframes=5))
y=datetime.datetime.now()
print(y-x)
#print(data)
print(data.shape)

print(img1.get_frames_status())

x = datetime.datetime.now()
data = np.array(img1.snap())
y=datetime.datetime.now()
print(y-x)
#print(data)
print(data.shape)
#print(img1.get_all_grabber_attribute_values())
print(img1.get_frames_status())

img1.start_acquisition(mode='sequence')
print('Started')
print(img1.get_frames_status())
img1.stop_acquisition()
print('Stopped')
print(img1.get_frames_status())
img1.clear_acquisition()
img1.clear_all_triggers()
img1.configure_trigger_in('ext', trig_line=0, trig_pol='high', trig_action='capture', timeout=5, reset_acquisition=True)
print('configured')
img1.serial_write('OPR?')
print(img1.serial_readline())
img1.serial_write('OPR 12')
print(img1.serial_readline())
img1.serial_write('OPR?')
print(img1.serial_readline())
img1.serial_write('TRIG:MODE?')
print(img1.serial_readline())
img1.serial_write('TRIG:MODE 1')
print(img1.serial_readline())
data = np.array(img1.snap())
print(img1.get_frames_status())
img1.serial_write('OPR?')
print(img1.serial_readline())
plt.figure()
plt.plot(np.average(data[::2,300:430],axis=0))
plt.plot(np.average(data[1::2,300:430],axis=0))
plt.show()

dtt = (np.average(data[::2,300:430],axis=0) - np.average(data[1::2,300:430],axis=0))/np.average(data[1::2,300:430],axis=0)
plt.figure()
plt.plot(dtt)
plt.show()

img1.close()



