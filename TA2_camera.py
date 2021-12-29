from ctypes import *
import os
import numpy as np
from enum import IntEnum
#from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot														#Qt code

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

class octoplus(): #(QObject):																				#Qt code
    def __init__(self):
        #super(QObject,self).__init__()   																	#Qt code
        libname= os.path.abspath('CamCmosOctUsb3.dll')
        self.dll = WinDLL(libname)
        self.pixels = 2048 # including dummy pixels
        self.num_pixels = 2048
        self.first_pixel = 0
        self.enable_contextual_data = 1
        self.circular_buffer = 1
        self.trigger_mode = 1					#IMPORTANT: trigger_mode is set to 4 during experiments | for testing code trigger_mode is set to 1 (due to limited access to laser)
        self.exposure_time = 132 # units of 10 ns 
        self.max_bulk_queue_number = 128
        self.line_period = 1111  # units of 10 ns
        self.pulse_width = 80  # units of 10 ns
        self.timeout = c_ulong(5000)	# 5 s
        self.iNbOfBuffer = c_size_t(30)
        self.ulNbCameras = c_ulong()
        self.ulIndex = c_ulong(0)
        self.CameraInfo = tCameraInfo()
        self.hCamera = c_void_p()
        self.ImageInfos = tImageInfos()
        self.lines_per_frame = 1
        
    # Combined methods to call camera
    def Initialize(self, lines_per_frame = 1000):	#Initialize takes in variable register: lines_per_frame
        self.lines_per_frame = lines_per_frame
        self.InitializeLibrary()
        self.UpdateCameraList() 
        self.GetCameraInfo()
        self.OpenCamera()
        self.WriteRegister(0x4F000000, self.enable_contextual_data)
        self.WriteRegister(0x4F000018, self.circular_buffer)
        self.WriteRegister(0x1210C, self.trigger_mode)
        self.WriteRegister(0x12108, self.exposure_time)
        self.WriteRegister(0x4F000010, self.max_bulk_queue_number)
        self.WriteRegister(0x12128, self.lines_per_frame)
        self.WriteRegister(0x12100, self.line_period)
        self.WriteRegister(0x1211C, self.pulse_width)
        self.SetImageParameters()
        self.probe = np.empty((self.lines_per_frame, self.pixels),dtype = np.dtype(np.uint16))
        return         
    
    #start_acquire = pyqtSignal()																			#Qt code
    #data_ready = pyqtSignal(np.ndarray,np.ndarray,int,int)													#Qt code
    #@pyqtSlot()																							#Qt code

    def Acquire(self):
        self.StartAcquisition()
        self.GetBuffer()
        self.Construct_Data_Vec()
        #self.data_ready.emit(self.probe,self.reference,self.first_pixel,self.num_pixels)					#Qt code
        return         

    def Construct_Data_Vec(self):
        raw_data = cast(self.ImageInfos.pDatas, POINTER(c_ushort))
        for row in range(self.lines_per_frame):
	        for col in range(self.pixels):
	            self.probe[row][col] = raw_data[row*self.pixels+col]
        self.reference = np.ones((self.lines_per_frame, self.pixels), dtype = np.uint16)	#no reference data from octoplus, this is filled with ones (dummy data)
    
    #_exit = pyqtSignal()																					#Qt code
    #@pyqtSlot()																							#Qt code

    def Exit(self):
        self.RequeueBuffer()
        self.StopAcquisition()
        self.FlushBuffers()
        self.CloseCamera()
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

