from ctypes import *
import os
import numpy as np
from enum import IntEnum
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot	
import time
from datetime import datetime
from math import ceil
import Tombak_control as tk

class tCameraInfo(Structure):
	_fields_ = [("pcID", c_char*260)]

class tImagePixelType(IntEnum):
    eUnknown = 0
    eMono8 = 1
    eMono10 = 2
    eMono11 = 3
    eMono12 = 4

    def __init__(self, value):
	    self._as_parameter = c_int(value)

class tContextDataPerLine(Structure):
    _fields_ = [("u16LineCounter", c_ushort),
                ("u16NbMissedTriggers", c_ushort)]

class tImageInfos(Structure):
    _fields_ = [("hBuffer", c_void_p),
	            ("pDatas", c_void_p),
				("iBufferSize", c_size_t),
				("iImageSize", c_size_t),
				("iOffsetX", c_size_t),
				("iImageWidth", c_size_t),
				("iImageHeight", c_size_t),
				("eImagePixelType", c_int),
				("iLinePitch", c_size_t),
				("iHorizontalFlip", c_ushort),
				("iNbMissedTriggers", c_ulonglong),
				("iNbLineLost", c_ulonglong),
				("iNbImageAcquired", c_ulonglong),
				("iFrameTriggerNbValidLines", c_ulonglong),
				("iCounterBufferStarvation", c_ulonglong)]

# variables to print the current day and time
now = datetime.now()


class octoplus(QObject):																				
    def __init__(self):
        super(QObject,self).__init__()   																	
        libname= os.path.abspath('CamCmosOctUsb3.dll')
        self.dll = WinDLL(libname)
        self.pixels = 2048 # including dummy pixels
        self.num_pixels = 2048
        self.first_pixel = 0
        self.enable_contextual_data = 0
        self.circular_buffer = 0
        self.trigger_mode = 4					# IMPORTANT: trigger_mode is set to 4 during experiments | trigger_mode is set to 1 when testing code (due to limited access to laser)
        self.exposure_time = 132 # units of 10 ns
        self.max_bulk_queue_number = 128
        self.line_period = 1101 # units of 10 ns	# line_period = (line period * 100) - 10, to avoid losing "valid lines per frame" | period doubled from 1101 b/c frequency was halved
        self.pulse_width = 80  # units of 10 ns
        self.timeout = c_ulong(60000)	# 10 s
        self.iNbOfBuffer = c_size_t(10)
        self.ulNbCameras = c_ulong()
        self.ulIndex = c_ulong(0)
        self.CameraInfo = tCameraInfo()
        self.hCamera = c_void_p()
        self.ImageInfos = tImageInfos()
        #self.ContextDataPerLine = tContextDataPerLine()
        self.lines_per_frame = 1
        self.readtest = 0
        self.num_frames = 1
        self.port = 'COM3'  #port for frame trigger on tombak | line trigger is port 'COM5'
        self.current_day_time = now.strftime("%m/%d/%Y %H:%M:%S")
        
    # Combined methods to call camera
    def Initialize(self, lines_per_frame = 1000):
        #self.lines_per_frame = lines_per_frame
        if lines_per_frame > 44998:         
		# 44998 is the maximum number of lines per frame that can occur without dropped lines (for 2Hz frame trigger)
		# Will have to be lowered (by how many lines, 2?) if the frame trigger rate is greater than this number (NEEDS REVIEW)
		# If the desired number of lines > 44998, the lines will be split into multiple images, due to a limitation of the linescan camera
            self.num_frames = ceil(lines_per_frame / 44998)
            self.lines_per_frame = int(lines_per_frame/self.num_frames)
        else:
            self.lines_per_frame = lines_per_frame
        
        # Set TOMBAK - 'COM3' is frame trigger port
        tk.Tombak_frame_initialise(45000)	# Input can be given by the user in terms of time instead of number of shots
        
        self.InitializeLibrary()
        self.UpdateCameraList() 
        self.GetCameraInfo()
        self.OpenCamera()
        #self.WriteRegister(0x4F000000, self.enable_contextual_data)	could this be the issue, and cause zeros to be added to the end of the buffer? - no
        #self.WriteRegister(0x4F000018, self.circular_buffer)
        self.WriteRegister(0x1210C, self.trigger_mode)
        self.WriteRegister(0x12108, self.exposure_time)
        #self.WriteRegister(0x4F000010, self.max_bulk_queue_number)
        self.WriteRegister(0x12128, self.lines_per_frame)
        self.WriteRegister(0x12100, self.line_period)
        self.WriteRegister(0x1211C, self.pulse_width)

		#Reading registers for debugging
        #print ("trigger mode: ")
        #self.ReadRegister(0x1210C, self.readtest)
        #print ("exposure_time: ")
        #self.ReadRegister(0x12108, self.readtest)
        #print ("max_bulk_queue_number: ")
        #self.ReadRegister(0x4F000010, self.readtest)
        #print ("lines_per_frame: ")
        #self.ReadRegister(0x12128, self.readtest)
        #print ("line_period: ")
        #self.ReadRegister(0x12100, self.readtest)
        #print ("pulse_width: ")
        #self.ReadRegister(0x1211C, self.readtest)
        #print ("enable_contextual_data: ")
        #self.ReadRegister(0x4F000000, self.readtest)

        self.SetImageParameters()
        return         
    
    start_acquire = pyqtSignal()																			
    #data_ready = pyqtSignal(np.ndarray,np.ndarray,int,int)
    data_ready = pyqtSignal(np.ndarray,int,int)	
    @pyqtSlot()																							
    def Acquire(self):
        self.StartAcquisition()
        self.GetBuffer()
        self.FrameData()
        #print ("missed triggers: ")
        #self.ReadRegister(0x12110, self.readtest)
        #start=time.time()
        self.Construct_Data_Vec()
        try:
            self.RequeueBuffer()
        except OSError:     # Print time of OSError, an error given when RequeueBuffer does not work
            print("RequeueBuffer error occured: ", self.current_day_time)
        self.StopAcquisition()
        self.FlushBuffers()

        count = 1
        while count < self.num_frames:  # looping acquisition through no. of frames
            count = count + 1
            self.StartAcquisition()
            self.GetBuffer()
            self.FrameData()
            self.Update_Data_Vec()          
            try:
                self.RequeueBuffer()
            except OSError:
                print("RequeueBuffer error occured: ", self.current_day_time)
            self.StopAcquisition()
            self.FlushBuffers()

        #end=time.time()
        #print(end-start)
        #self.RequeueBuffer()
        #self.data_ready.emit(self.probe,self.reference,self.first_pixel,self.num_pixels)

		#Save to file
        #start = time.time()
        #np.savetxt('test_data.csv', self.probe, '%d')
        #end = time.time()
        #print("Time to save file: ",end-start)

        self.data_ready.emit(self.probe,self.first_pixel,self.num_pixels)
        #self.StopAcquisition()
        #self.FlushBuffers()
        return 

    def Construct_Data_Vec(self):
        raw_data = cast(self.ImageInfos.pDatas, POINTER(c_ushort))
        self.probe = np.ctypeslib.as_array(raw_data, shape = (self.lines_per_frame, self.pixels))
        #self.reference = np.ones((self.lines_per_frame, self.pixels), dtype = np.uint16)

    def Update_Data_Vec(self):
        raw_data = cast(self.ImageInfos.pDatas, POINTER(c_ushort))
        probe = np.ctypeslib.as_array(raw_data, shape = (self.lines_per_frame, self.pixels))
        self.probe = np.append(self.probe, probe, axis = 0)

    def FrameData(self):		
        if self.ImageInfos.iFrameTriggerNbValidLines!= 0 and self.ImageInfos.iFrameTriggerNbValidLines!=self.lines_per_frame:
            #print("Images Acquired: ", self.ImageInfos.iNbImageAcquired)
            print("Lines lost: ", self.ImageInfos.iNbLineLost)
            print("Missed triggers: ", self.ImageInfos.iNbMissedTriggers)
            print("Valid lines from frame: ", self.ImageInfos.iFrameTriggerNbValidLines)
        if self.ImageInfos.iCounterBufferStarvation!= 0:
            print("Buffer Starvation!!!!!")
      	

    _exit = pyqtSignal()																				
    @pyqtSlot()																						
    def Exit(self):
        #self.StopAcquisition()
        #self.FlushBuffers()
        self.CloseCamera()
        print("Camera Closed")
        self.TerminateLibrary()
        
    ###########################################################################
    ###########################################################################
    ###########################################################################
    #Library methods from DLL (Do not Edit)

    def InitializeLibrary(self):
        self.dll.USB3_InitializeLibrary.restype = None
        self.dll.USB3_InitializeLibrary()

    def UpdateCameraList(self):
        self.dll.USB3_UpdateCameraList.restype = c_ulong
        self.dll.USB3_UpdateCameraList(byref(self.ulNbCameras))

    def GetCameraInfo(self):
        self.dll.USB3_GetCameraInfo.restype = POINTER(tCameraInfo)
        self.dll.USB3_GetCameraInfo(self.ulIndex, byref(self.CameraInfo))

    def OpenCamera(self):
        self.dll.USB3_OpenCamera.restype = c_void_p
        self.dll.USB3_OpenCamera(byref(self.CameraInfo), byref(self.hCamera))
        
    def WriteRegister(self, nAddress, nValue):
        ulAddress = c_ulong(nAddress)
        ulValue = c_ulong(nValue)
        iSize = c_size_t(ulValue.__sizeof__())
        self.dll.USB3_WriteRegister.restype = c_size_t
        self.dll.USB3_WriteRegister(self.hCamera, ulAddress, byref(ulValue), byref(iSize))

    def ReadRegister(self, nAddress, nValue):
        ulAddress = c_ulong(nAddress)
        ulValue = c_ulong(nValue)
        iSize = c_size_t(ulValue.__sizeof__())
        self.dll.USB3_ReadRegister.restype = c_size_t
        self.dll.USB3_ReadRegister(self.hCamera, ulAddress, byref(ulValue), byref(iSize))
        print(ulValue.value)
        
    def SetImageParameters(self):
        iImageHeight = c_size_t(self.lines_per_frame)
        self.dll.USB3_SetImageParameters.restype = None
        self.dll.USB3_SetImageParameters(self.hCamera, iImageHeight, self.iNbOfBuffer)

    def StartAcquisition(self):
        self.dll.USB3_StartAcquisition.restype = None
        self.dll.USB3_StartAcquisition(self.hCamera)

    def GetBuffer(self):
        self.dll.USB3_GetBuffer.restype = POINTER(tImageInfos)
        self.dll.USB3_GetBuffer(self.hCamera, byref(self.ImageInfos), self.timeout)

    def GetLineContextualData(self):
        self.dll.USB3_GetLineContextualData.restype = POINTER(tContextDataPerLine)
        self.dll.USB3_GetLineContextualData(self.hCamera, byref(self.ImageInfos), byref(self.ContextDataPerLine), self.ulLineNumber)
        print(ContextDataPerLine.u16NbMissedTriggers)

    def RequeueBuffer(self):
        self.dll.USB3_RequeueBuffer.argtypes = [c_void_p, c_void_p]
        self.dll.USB3_RequeueBuffer.restype = None
        self.dll.USB3_RequeueBuffer(self.hCamera, self.ImageInfos.hBuffer)

    def StopAcquisition(self):
        self.dll.USB3_StopAcquisition.restype = None
        self.dll.USB3_StopAcquisition(self.hCamera)

    def FlushBuffers(self):
        self.dll.USB3_FlushBuffers.restype = None
        self.dll.USB3_FlushBuffers(self.hCamera)

    def CloseCamera(self):
        self.dll.USB3_CloseCamera.restype = None
        self.dll.USB3_CloseCamera(self.hCamera)

    def TerminateLibrary(self):
        self.dll.USB3_TerminateLibrary.restype = None
        self.dll.USB3_TerminateLibrary()

