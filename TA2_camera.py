from ctypes import *
import os
import numpy as np
from enum import IntEnum
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot	
import time

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

class octoplus(QObject):																				
    def __init__(self):
        super(QObject,self).__init__()   																	
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
        self.timeout = c_ulong(10000)	# 10 s
        self.iNbOfBuffer = c_size_t(30)
        self.ulNbCameras = c_ulong()
        self.ulIndex = c_ulong(0)
        self.CameraInfo = tCameraInfo()
        self.hCamera = c_void_p()
        self.ImageInfos = tImageInfos()
        self.lines_per_frame = 1
        self.readtest = 0
        
    # Combined methods to call camera
    def Initialize(self, lines_per_frame = 1000):
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

		#Reading resgisters for debugging
        print ("trigger mode: ")
        self.ReadRegister(0x1210C, self.readtest)
        print ("exposure_time: ")
        self.ReadRegister(0x12108, self.readtest)
        print ("max_bulk_queue_number: ")
        self.ReadRegister(0x4F000010, self.readtest)
        print ("lines_per_frame: ")
        self.ReadRegister(0x12128, self.readtest)
        print ("line_period: ")
        self.ReadRegister(0x12100, self.readtest)
        print ("pulse_width: ")
        self.ReadRegister(0x1211C, self.readtest)
        print ("enable_contextual_data: ")
        self.ReadRegister(0x4F000000, self.readtest)

        self.SetImageParameters()
        return         
    
    start_acquire = pyqtSignal()																			
    #data_ready = pyqtSignal(np.ndarray,np.ndarray,int,int)
    data_ready = pyqtSignal(np.ndarray,int,int)	
    @pyqtSlot()																							
    def Acquire(self):
        self.StartAcquisition()
        self.GetBuffer()
        print ("missed triggers: ")
        self.ReadRegister(0x12110, self.readtest)
        start=time.time()
        self.Construct_Data_Vec()
        end=time.time()
        #print(end-start)
        self.RequeueBuffer()
        #self.data_ready.emit(self.probe,self.reference,self.first_pixel,self.num_pixels)	
        self.data_ready.emit(self.probe,self.first_pixel,self.num_pixels)
        #self.StopAcquisition()
        #self.FlushBuffers()
        return 

    def Construct_Data_Vec(self):
        raw_data = cast(self.ImageInfos.pDatas, POINTER(c_ushort))
        self.probe = np.ctypeslib.as_array(raw_data, shape = (self.lines_per_frame, self.pixels))
        #self.reference = np.ones((self.lines_per_frame, self.pixels), dtype = np.uint16)	#no reference data from octoplus, this is filled with ones (dummy data)

    _exit = pyqtSignal()									#commenting to test if the code runs less/more efficiently or if changes are negligible												
    @pyqtSlot()																						
    def Exit(self):
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

    def RequeueBuffer(self):
        self.dll.USB3_RequeueBuffer.argtypes = c_void_p, c_void_p
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

