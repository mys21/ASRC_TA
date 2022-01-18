from ctypes import *
import os
from enum import IntEnum
import numpy as np


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



class octoplus:
    def __init__(self):
        libname= os.path.abspath('CamCmosOctUsb3.dll')
        self.c_lib = WinDLL(libname)
        self.first_pixel = 0
        self.num_pixels = 2048
        self.ulNbCameras = c_ulong()
        self.ulIndex = c_ulong(0)
        self.CameraInfo = tCameraInfo()
        self.hCamera = c_void_p()
        self.ImageInfos = tImageInfos()
        self.iNbOfBuffer = c_size_t(30)
        self.timeout = c_ulong(3000)



    def Initialize(self):
        self.InitializeLibrary()
        self.UpdateCameraList()
        self.GetCameraInfo()
        self.OpenCamera()
        self.WriteRegister(0x1210C, 1)
        self.WriteRegister(0x12100, 1111)
        self.SetImageParameters()

    def Acquire(self):
        self.StartAcquisition()
        self.GetBuffer()

    def InitializeLibrary(self):
        self.c_lib.USB3_InitializeLibrary.restype = None
        self.c_lib.USB3_InitializeLibrary()

    def UpdateCameraList(self):
        self.c_lib.USB3_UpdateCameraList.restype = c_ulong
        self.c_lib.USB3_UpdateCameraList(byref(self.ulNbCameras))
        print('Number of Cameras: ', self.ulNbCameras.value)

    def GetCameraInfo(self):
        self.c_lib.USB3_GetCameraInfo.restype = POINTER(tCameraInfo) 
        self.c_lib.USB3_GetCameraInfo(self.ulIndex,byref(self.CameraInfo)) 
        print("Camera ID: ", self.CameraInfo.pcID)	

    def OpenCamera(self):
        self.c_lib.USB3_OpenCamera.restype = c_void_p
        self.c_lib.USB3_OpenCamera(byref(self.CameraInfo), byref(self.hCamera)) 

	#Registers
	##############################################################################

    def WriteRegister(self, nAddress, nValue):
        self.c_lib.USB3_WriteRegister.restype = c_size_t
        ulAddress= c_ulong(nAddress) 
        ulValue = c_ulong(nValue)
        iSize = c_size_t(ulValue.__sizeof__())
        self.c_lib.USB3_WriteRegister(self.hCamera, ulAddress, byref(ulValue), byref(iSize))

    def SetImageParameters(self):
        self.c_lib.USB3_SetImageParameters(self.hCamera, self.ImageInfos.iImageHeight, self.iNbOfBuffer)

    def StartAcquisition(self):
        self.c_lib.USB3_StartAcquisition(self.hCamera)

    def GetBuffer(self):
        self.c_lib.USB3_GetBuffer.restype = POINTER(tImageInfos)
        self.c_lib.USB3_GetBuffer(self.hCamera, byref(self.ImageInfos), self.timeout)
        print('Buffer Size: ', self.ImageInfos.iBufferSize)






