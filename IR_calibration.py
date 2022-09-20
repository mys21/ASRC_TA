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


#img1 = IMAQ.IMAQ.IMAQFrameGrabber(imaq_name='img0')
img1 = IMAQ.IMAQ.IMAQCamera(name='img0')
img1.open()
img1.set_grabber_attribute_value('IMG_ATTR_ACQWINDOW_HEIGHT',5000,'auto')
img1.setup_serial_params('\r','str')
#img1.serial_write('OPR 12')
#print(img1.serial_readline())
#img1.serial_write('TRIG:MODE 1')
#print(img1.serial_readline())
img1.configure_trigger_in('ext', trig_line=0, trig_pol='high', trig_action='capture', timeout=5, reset_acquisition=True)
num_frames=100
#data = np.array(img1.snap())
img1.start_acquisition()
img1.wait_for_frame(nframes=num_frames)
finfo = img1.get_frames_status()
data = img1.read_multiple_images()
img1.stop_acquisition()
print(np.array(data).shape)
print(finfo)
data1 = np.array(data,dtype=float)
data2 = data1.reshape(5000*finfo[1],1024)
print(np.array(data2).shape)
savename = 'D:\IR_testing/360k_shots_IRcamera.txt'
#np.savetxt(savename, data2)
#print(data)
#img1.serial_write('OPR?')
#print(img1.serial_readline())
#print(img1.serial_readline())

plt.figure()
plt.plot(np.average(data2,axis=0))
avg = np.average(data2,axis=0)
plt.show()


savename = 'D:\IR_CalibrationLamp.txt'
np.savetxt(savename, avg)

plt.show()

img1.close()
del img1


