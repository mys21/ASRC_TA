#from ctypes import *
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

num_lines = 3000
num_frames = 13
cam1 = IMAQ.IMAQCamera(name='img0')
cam1.open()
cam1.set_grabber_attribute_value('IMG_ATTR_ACQWINDOW_HEIGHT',num_lines,'auto')
cam1.configure_trigger_in('ext', trig_line=1, trig_pol='high', trig_action='capture', timeout=5, reset_acquisition=True)
cam1.setup_serial_params('\r','str')
data = np.array(cam1.snap())
#cam1.start_acquisition()
cam1.wait_for_frame(nframes=num_frames)
cam1.close()
del cam1



#img1.setup_serial_params('\r','str')
#img1.serial_write('OPR 12')
#print(img1.serial_readline())
#img1.serial_write('TRIG:MODE 1')
#print(img1.serial_readline())
#img1.configure_trigger_in('ext', trig_line=0, trig_pol='high', trig_action='capture', timeout=5, reset_acquisition=True)
#num_frames=1
#data = np.array(img1.snap())
#img1.start_acquisition()
#img1.wait_for_frame(nframes=num_frames)
#finfo = img1.get_frames_status()
#data = img1.read_multiple_images()
#img1.stop_acquisition()
#print(np.array(data).shape)
#print(finfo)
#data1 = np.array(data,dtype=int)
#data2 = data1.reshape(num_lines*finfo[1],1024)
#print(np.array(data2).shape)
#savename = 'D:\IR_testing_new.txt'
#np.savetxt(savename, data2)
#print(data)
#img1.serial_write('OPR?')
#print(img1.serial_readline())
#print(img1.serial_readline())

#plt.figure()
#plt.plot(np.average(data2[::3,:],axis=0))
#plt.plot(np.average(data2[1::3,:],axis=0))
#plt.show()

#probe1_on_array = data2[1::6,:]
#probe1_off_array = data2[2::6,:]
#probe2_off_array = data2[3::6,:]
#probe2_on_array = data2[4::6,:]

#probe_on_array = data2[::3,:]
#probe_off_array = data2[1::3,:]

#dtt_array = np.divide(((probe1_on_array + probe2_on_array) - (probe1_off_array + probe2_off_array)), (probe1_off_array + probe2_off_array))
#dt_array = (probe1_on_array + probe2_on_array) - (probe1_off_array + probe2_off_array)

#dtt_array = np.divide((probe_on_array  - probe_off_array ), probe_off_array, out=(probe_on_array  - probe_off_array ), where=probe_off_array!=0 )
#dt_array = probe_on_array - probe_off_array 

#dt1 = (data2[0,:] - data2[1,:])

#dtt = (np.average(data2[::3,:],axis=0) - np.average(data2[1::3,:],axis=0))/np.average(data2[1::2,:],axis=0)
#dt = np.average(data2[::3,:],axis=0) - np.average(data2[1::3,:],axis=0)

#dt = np.average(dt_array,axis=0)
#dtt = np.average(dtt_array,axis=0)

#plt.figure()
#plt.plot(dt)
#plt.plot(dtt)

#savename = 'D:\IR_testing_39k_shots_IRcamera_data_int.txt'
#np.savetxt(savename, data2, fmt='%.4e')

#plt.show()

#img1.close()



