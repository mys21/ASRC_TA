from ctypes import *
import os
import numpy as np
from enum import IntEnum
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

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
        self.dll = ct.WinDLL(r"C:\Users\mysfe\OneDrive\Desktop\ASRC_TA\CamCmosOctUsb3.dll")
        self.pixels = 2048 #including dummy pixels
        self.num_pixels = 2048
        self.first_pixel = 0
        self.enable_contextual_data = 1
        self.circular_buffer = 1
        self.trigger_mode = 4
        self.exposure_time = 132 # units of 10 ns 
        self.max_bulk_queue_number = 128
        self.line_period = 1111  # units of 10 ns
        self.pulse_width = 80  # units of 10 ns
        self.timeout = c_ulong(3000)
        self.iNbOfBuffer = c_size_t(30)
        self.ulNbCameras = c_ulong()
        
    #Combined methods to call camera
    def Initialize(self, lines_per_frame = 45000):
        self.lines_per_frame = lines_per_frame
        self.InitializeLibrary()

        ulNbCameras= c_ulong()
        self.UpdateCameraList(byref(ulNbCameras))
        print('Number of Cameras: ',ulNbCameras.value)
 
        ulIndex= c_ulong(0) 
        CameraInfo = tCameraInfo()
        self.GetCameraInfo(ulIndex,byref(CameraInfo))
        print("Camera ID: ", CameraInfo.pcID)

        hCamera=c_void_p()
        OpenCamera(byref(CameraInfo), byref(hCamera))

        ulAddress= c_ulong(0x4F000000) 
        ulValue = c_ulong(self.enable_contextual_data)
        iSize = c_size_t(ulValue.__sizeof__())
        self.WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))

        ulAddress= c_ulong(0x4F000018) 
        ulValue = c_ulong(self.circular_buffer)
        self.WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))

        ulAddress= c_ulong(0x1210C)
        ulValue = c_ulong(self.trigger_mode)
        self.WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))

        ulAddress= c_ulong(0x12108) 
        ulValue = c_ulong(self.exposure_time)
        self.WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))

        ulAddress= c_ulong(0x4F000010) 
        ulValue = c_ulong(self.max_bulk_queue_number)
        self.WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))

        ulAddress= c_ulong(0x12128) 
        ulValue = c_ulong(self.lines_per_frame)
        self.WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))

        ulAddress= c_ulong(0x12100) 
        ulValue = c_ulong(self.line_period)
        self.WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))

        ulAddress= c_ulong(0x1211C) 
        ulValue = c_ulong(self.pulse_width)
        self.WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))

        iImageHeight = c_size_t(self.lines_per_frame)
        iNbOfBuffer = c_size_t(30)

        self.SetImageParameters(hCamera, iImageHeight, iNbOfBuffer)
        self.array = np.zeros((self.lines_per_frame,self.pixels*2),dtype=np.dtype(np.int16))
        return         
    
    start_acquire = pyqtSignal()
    data_ready = pyqtSignal(np.ndarray,np.ndarray,int,int)
    @pyqtSlot()
    def Acquire(self):
        self.GetBuffer(hCamera, ImageInfos, timeout)
        self.Construct_Data_Vec()
        self.data_ready.emit(self.probe,self.reference,self.first_pixel,self.num_pixels)
        return         

    def Construct_Data_Vec(self, ImageInfos):
        raw_data = cast(ImageInfos.pDatas, POINTER(c_ushort))
        for row in range(lines_per_frame):
	        for col in range(pixels):
	            self.probe[row][col] = raw_data[row*pixels+col]
	#reference data - there is no reference data from octoplus, this is filled with ones (dummy data)
        self.reference = np.ones(lines_per_frame, pixels, dtype = uint16)
    
    _exit = pyqtSignal()
    @pyqtSlot()
    def Exit(self):
        self.CCDDrvExit()
        
    ###########################################################################
    ###########################################################################
    ###########################################################################
    #Library methods from DLL (Do not Edit)

    def InitializeLibrary(self):
        self.dll.USB3_InitializeLibrary.restype = None
        self.dll.USB3_InitializeLibrary()

    def UpdateCameraList(self, pulNbCameras):
        self.dll.USB3_UpdateCameraList.restype = c_ulong
        self.dll.USB3_UpdateCameraList(pulNbCameras)

    def GetCameraInfo(self, ulIndex, pCameraInfo):
        self.dll.USB3_GetCameraInfo.restype = POINTER(tCameraInfo)
        self.dll.USB3_GetCameraInfo(ulIndex,pCameraInfo)

    def OpenCamera(self, CameraInfo, hCamera):
        self.dll.USB3_OpenCamera.restype = c_void_p
        self.dll.USB3_OpenCamera(byref(CameraInfo), byref(hCamera))
        
    def WriteRegister(self, hCamera, ulAddress, ulValue, piSize):
        self.dll.USB3_WriteRegister.restype = c_size_t
        self.dll.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))

    def SetImageParameters(self, hCamera, iImageHeight, iNbOfBuffer):
        self.dll.USB3_SetImageParameters.restype = None
        self.dll.USB3_SetImageParameters(hCamera, iImageHeight, iNbOfBuffer)

    def StartAcquisition(self, hCamera):
        self.dll.USB3_StartAcquisition.restype = None
        self.dll.USB3_StartAcquisition(hCamera)

    def GetBuffer(self, hCamera, ImageInfos, timeout):
        self.dll.GetBuffer.restype = tImageInfos
        self.dll.USB3_GetBuffers(hCamera, byref(ImageInfos), timeout)

    def RequeueBuffer(self, hCamera, iImageHeight, iNbOfBuffer):
        self.dll.USB3_RequeueBuffer.argtypes = [c_void_p, c_void_p]
        self.dll.USB3_RequeueBuffer.restype = None
        self.dll.USB3_RequeueBuffer(hCamera, ImageInfos.hBuffer)

    def StopAcquisition(self, hCamera):
        self.dll.USB3_StopAcquisition.restype = None
        self.dll.USB3_StopAcquisition(hCamera)

    def FlushBuffers(self, hCamera):
        self.dll.USB3_FlushBuffers.restype = None
        self.dll.USB3_FlushBuffers(hCamera)

    def CloseCamera(self, hCamera):
        self.dll.USB3_CloseCamera.restype = None
        self.dll.USB3_CloseCamera(hCamera)

    def TerminateLibrary(self):
        self.dll.USB3_TerminateLibrary.restype = None
        self.dll.USB3_TerminateLibrary()

