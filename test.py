#import ctypes
from ctypes import *
import os

class tCameraInfo(Structure):
	_fields_ = [("pcID", c_char*260)]
	


if __name__ == "__main__":
    libname= os.path.abspath('CamCmosOctUsb3.dll')
    c_lib = CDLL(libname) #cdll loads libraries which export functions using the standard cdecl calling convension, as opposed to other things, and this is what we need

    c_lib.USB3_InitializeLibrary.restype = None
    c_lib.USB3_InitializeLibrary()

    ulNbCameras= c_ulong()
    c_lib.USB3_UpdateCameraList.restype = c_ulong
    c_lib.USB3_UpdateCameraList(byref(ulNbCameras))
    print('Number of Cameras: ',ulNbCameras.value)	#Works

    ulIndex= c_ulong(0)
    CameraInfo = tCameraInfo()
    c_lib.USB3_GetCameraInfo.restype = c_char*260
    c_lib.USB3_GetCameraInfo(ulIndex,byref(CameraInfo))

    hCamera=c_void_p()
    c_lib.USB3_OpenCamera.restype = c_void_p
    c_lib.USB3_OpenCamera(byref(CameraInfo), byref(hCamera))

	#Writing to registers
    c_lib.USB3_WriteRegister.restype = c_size_t
    ulAddress= c_ulong(0x12128) 
    ulValue = c_ulong(45000)  #lines per frame
    iSize = c_size_t(ulValue.__sizeof__())
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Lines per frame: ', ulValue.value)

    ulAddress= c_ulong(0x12108) 
    ulValue = c_ulong(132)  #exposure time
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Exposure time: ', ulValue.value)

    ulAddress= c_ulong(0x1210C) 
    ulValue = c_ulong(4)  #trigger mode
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Trigger mode: ', ulValue.value)

    ulAddress= c_ulong(0x4F000018) 
    ulValue = c_ulong(1)  #circular buffer on or off
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Circular buffer: ', ulValue.value)

    ulAddress= c_ulong(0x4F000010) 
    ulValue = c_ulong(16)  #max bulk queue number
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Max bulk queue number: ', ulValue.value)

    ulAddress= c_ulong(0x4F000000) 
    ulValue = c_ulong(1)  #contextual data on or off
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Contextual data: ', ulValue.value)

    ulAddress= c_ulong(0x12100) 
    ulValue = c_ulong(1111)  #line period x 10^(-8) seconds
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Line period: ', ulValue.value)

    ulAddress= c_ulong(0x1211C) 
    ulValue = c_ulong(80)  #pulse width discriminator x 10^(-8) seconds
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Pulse width: ', ulValue.value)


else:
    print("Error")
	
