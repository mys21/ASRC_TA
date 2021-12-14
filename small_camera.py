#need to make all the other variables self.
from ctypes import *
import os
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class tCameraInfo(Structure):
	_fields_ = [("pcID", c_char*260)]

class camera1(QObject):
	def __init__(self):
		super(QObject,self).__init__()
		self.libname= os.path.abspath('CamCmosOctUsb3.dll')
		self.c_lib = CDLL(self.libname)
		#cdll loads libraries which export functions using the standard cdecl calling convension, as opposed to other things, and this is what we need
		self.something = "camera object initialized"

	def Initialize(self, number_of_scans=100, line_period=9):
	    self.c_lib.USB3_InitializeLibrary.restype = None
	    self.c_lib.USB3_InitializeLibrary()

	    ulNbCameras= c_ulong()
	    self.c_lib.USB3_UpdateCameraList.restype = c_ulong
	    self.c_lib.USB3_UpdateCameraList(byref(ulNbCameras))
	    print('Number of Cameras: ',ulNbCameras.value)	#Works

	    ulIndex= c_ulong(0)
	    CameraInfo = tCameraInfo()
	    self.c_lib.USB3_GetCameraInfo.restype = c_char*260
	    self.c_lib.USB3_GetCameraInfo(ulIndex,byref(CameraInfo))

	    hCamera=c_void_p()
	    self.c_lib.USB3_OpenCamera.restype = c_void_p
	    self.c_lib.USB3_OpenCamera(byref(CameraInfo), byref(hCamera))

		#Writing to registers
	    self.c_lib.USB3_WriteRegister.restype = c_size_t

			# dynamic
	    ulAddress= c_ulong(0x12128)
	    ulValue = c_ulong(45000)  #lines per frame
	    iSize = c_size_t(ulValue.__sizeof__())
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    print('Lines per frame: ', ulValue.value)

	    ulAddress= c_ulong(0x12100)
	    ulValue = c_ulong(1111)  #line period x 10^(-8) seconds
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    print('Line period: ', ulValue.value)

			#fixed
	    ulAddress= c_ulong(0x12108)
	    ulValue = c_ulong(132)  #exposure time
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    print('Exposure time: ', ulValue.value)

	    ulAddress= c_ulong(0x1210C)
	    ulValue = c_ulong(4)  #trigger mode
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    print('Trigger mode: ', ulValue.value)

	    ulAddress= c_ulong(0x4F000018)
	    ulValue = c_ulong(1)  #circular buffer on or off
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    print('Circular buffer: ', ulValue.value)

	    ulAddress= c_ulong(0x4F000010)
	    ulValue = c_ulong(16)  #max bulk queue number
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    print('Max bulk queue number: ', ulValue.value)

	    ulAddress= c_ulong(0x4F000000)
	    ulValue = c_ulong(1)  #contextual data on or off
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    print('Contextual data: ', ulValue.value)

	    ulAddress= c_ulong(0x1211C)
	    ulValue = c_ulong(80)  #pulse width discriminator x 10^(-8) seconds
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    print('Pulse width: ', ulValue.value)
	    self.something2 = "camera itself initialized!"
