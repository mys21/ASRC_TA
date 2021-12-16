#need to make all the other variables self.
from ctypes import *
import os
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class tCameraInfo(Structure):
	_fields_ = [("pcID", c_char*260)]

class camera1(QObject):
	def __init__(self):
		super(QObject,self).__init__()
		#self.libname= os.path.abspath('CamCmosOctUsb3.dll')
		#self.c_lib = CDLL(self.libname)
		#cdll loads libraries which export functions using the standard cdecl calling convension, as opposed to other things, and this is what we need
		self.c_lib=WinDLL(r"C:\Users\mysfe\OneDrive\Desktop\ASRC_TA\CamCmosOctUsb3.dll")
		self.log = ["camera object initialized"]

	def Initialize(self, line_period=1111, number_of_scans=45000):
	    self.c_lib.USB3_InitializeLibrary.restype = None
	    self.c_lib.USB3_InitializeLibrary()

	    ulNbCameras= c_ulong()
	    self.c_lib.USB3_UpdateCameraList.restype = c_ulong
	    self.c_lib.USB3_UpdateCameraList(byref(ulNbCameras))
	    self.log.append('Number of Cameras: ' + str(ulNbCameras.value))	#Works

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
	    ulValue = c_ulong(number_of_scans)  #lines per frame
	    iSize = c_size_t(ulValue.__sizeof__())
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    self.log.append('Lines per frame: '+ str(ulValue.value))

	    ulAddress= c_ulong(0x12100)
	    ulValue = c_ulong(line_period)  #line period x 10^(-8) seconds
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    self.log.append('Line period: '+ str(ulValue.value))

			#fixed
	    ulAddress= c_ulong(0x12108)
	    ulValue = c_ulong(132)  #exposure time
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    self.log.append('Exposure time: '+ str(ulValue.value))

	    ulAddress= c_ulong(0x1210C)
	    ulValue = c_ulong(4)  #trigger mode
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    self.log.append('Trigger mode: '+ str(ulValue.value))

	    ulAddress= c_ulong(0x4F000018)
	    ulValue = c_ulong(1)  #circular buffer on or off
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    self.log.append('Circular buffer: '+ str(ulValue.value))

	    ulAddress= c_ulong(0x4F000010)
	    ulValue = c_ulong(16)  #max bulk queue number
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    self.log.append('Max bulk queue number: '+ str(ulValue.value))

	    ulAddress= c_ulong(0x4F000000)
	    ulValue = c_ulong(1)  #contextual data on or off
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    self.log.append('Contextual data: '+ str(ulValue.value))

	    ulAddress= c_ulong(0x1211C)
	    ulValue = c_ulong(80)  #pulse width discriminator x 10^(-8) seconds
	    self.c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
	    self.log.append('Pulse width: '+ str(ulValue.value))
	    self.log.append("camera itself initialized!")
