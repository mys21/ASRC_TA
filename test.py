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
				("iCounterBufferStarvation", c_ulonglong),]


if __name__ == "__main__":
    libname= os.path.abspath('CamCmosOctUsb3.dll')
    c_lib = WinDLL(libname) #cdll loads libraries which export functions using the standard cdecl calling convension, as opposed to other things, and this is what we need
  
	#Initialize Camera
	##############################################################################
	##############################################################################

    c_lib.USB3_InitializeLibrary.restype = None
    c_lib.USB3_InitializeLibrary()

    ulNbCameras = c_ulong()
    c_lib.USB3_UpdateCameraList.restype = c_ulong
    c_lib.USB3_UpdateCameraList(byref(ulNbCameras))
    print('Number of Cameras: ',ulNbCameras.value)

    ulIndex = c_ulong(0) 
    CameraInfo = tCameraInfo()
    c_lib.USB3_GetCameraInfo.restype = POINTER(tCameraInfo) 
    c_lib.USB3_GetCameraInfo(ulIndex,byref(CameraInfo)) 
    print("Camera ID: ", CameraInfo.pcID)	

    hCamera = c_void_p()
    c_lib.USB3_OpenCamera.restype = c_void_p
    c_lib.USB3_OpenCamera(byref(CameraInfo), byref(hCamera)) 

	#Fixed Registers
	##############################################################################

    c_lib.USB3_WriteRegister.restype = c_size_t
    ulAddress= c_ulong(0x1210C) 
    ulValue = c_ulong(1)  #trigger mode
    iSize = c_size_t(ulValue.__sizeof__())
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Trigger mode: ', ulValue.value)

    ulAddress= c_ulong(0x12108) 
    ulValue = c_ulong(132)  #exposure time
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Exposure time: ', ulValue.value)

    ulAddress= c_ulong(0x4F000010) 
    ulValue = c_ulong(128)  #max bulk queue number
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Max bulk queue number: ', ulValue.value)

    ulAddress= c_ulong(0x12100) 
    ulValue = c_ulong(1111)  #line period x 10^(-8) seconds
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Line period: ', ulValue.value)

    ulAddress= c_ulong(0x1211C) 
    ulValue = c_ulong(80)  #pulse width discriminator x 10^(-8) seconds
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Pulse width: ', ulValue.value)

	#Dynamic Register
	##############################################################################

    lines_per_frame = 1000
    ulAddress= c_ulong(0x12128) 
    ulValue = c_ulong(lines_per_frame)
    c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
    print('Lines per frame: ', ulValue.value)

    iImageHeight = c_size_t(lines_per_frame)
    iNbOfBuffer = c_size_t(30)

    c_lib.USB3_SetImageParameters(hCamera, iImageHeight, iNbOfBuffer)

	#Start Acquisition - "def Acquire"
	##############################################################################
	##############################################################################

    c_lib.USB3_StartAcquisition(hCamera)

	#"ReadFFLoop"
	##############################################################################

    ImageInfos = tImageInfos()
    timeout = c_ulong(3000) #timeout in 30000 ms
    c_lib.USB3_GetBuffer.restype = POINTER(tImageInfos)
    c_lib.USB3_GetBuffer(hCamera, byref(ImageInfos), timeout)
    print('Buffer Size: ', ImageInfos.iBufferSize)

	#"Construct_Data_Vec"
	##############################################################################
	
    #self.pixels
    pixels = 2048
	
    #self.data - 
    probe = np.empty((lines_per_frame,pixels), dtype = np.dtype(np.uint16))
    reference = np.ones((lines_per_frame, pixels), dtype = np.dtype(np.uint16))
	
    def CopyBuffer(ImageInfos, probe):
        raw_data = cast(ImageInfos.pDatas, POINTER(c_ushort))
        for row in range(lines_per_frame):
	        for col in range(pixels):
	            probe[row][col] = raw_data[row*pixels+col]
        print("Values", probe)
        print("Max val: ", np.max(probe))
        #index = np.where(data==np.max(data))
        #print('Coordinates of max value: ')
        #coordinates = list(zip(index[0], index[1]))    # zip the 2 arrays to get the exact coordinates
        # travese over the list of cordinates
        #for cord in coordinates:
            #print(cord)
        print("Min val: ", np.min(probe))
        print("Average val: ", np.average(probe))
        return

	#Acquire readable data in matrix form
    CopyBuffer(ImageInfos, probe)

	#Construct_Data - how will this change the data from the 2d array?
	##############################################################################

    

    #def Construct_Data_Vec(data):
        # dtype of self.data is uint32
        #hiloArray = data.view(np.uint16)[:,0:pixels*2]  # temp = shots x (2*pixels)

        #print (hiloArray.shape)
        # either:        
        #d = hiloArray.shape;
        #self.probe     = hiloArray[:,0:(d[-1]/2)]
        #self.reference = hiloArray[:,(d[-1]/2+1):d[-1]]
        # or: (easier to read)
        #hiloArray = hiloArray.reshape(hiloArray.shape[0],2,pixels)	#need twice the number of pixels in hiloarray before shape is changed to another dimension
        #reference = np.ones(shape(probe, unit16))
        #print("Reference: ", reference)
        #reference = hiloArray[:,1,:]

	#"class ta_processing_data"
	##############################################################################
	##############################################################################
	
	#"def __init__"
	##############################################################################
	
    first_pixel = 0
    num_pixels = 2048

    untrimmed_probe_array = np.array(probe,dtype=int)
    probe_array = np.array(probe,dtype=float)[:,first_pixel:num_pixels+first_pixel]
    reference_array = np.array(reference,dtype=float)[:,first_pixel:num_pixels+first_pixel]
    raw_probe_array = np.array(probe,dtype=float)[:,first_pixel:num_pixels+first_pixel]
    raw_reference_array = np.array(reference,dtype=float)[:,first_pixel:num_pixels+first_pixel]

	#"def seperate_on_off"
	##############################################################################

     #   '''separates on and off shots in the probe and reference arrays, note that
     #     when the tau flip is passed as true (long time shots where the delay was 
     #    offset by 1ms) the trigger is rolled over by one value to compensate. 
     #    Should get rid of tau flip'''

    high_std = False
    tau_flip_request = True
	
    if tau_flip_request is True:
        probe_on_array = probe_array[::2,:]
        probe_off_array = probe_array[1::2,:]
        reference_on_array = reference_array[::2,:]
        reference_off_array = reference_array[1::2,:]
    else:
        probe_on_array = probe_array[1::2,:]
        probe_off_array = probe_array[::2,:]
        reference_on_array = reference_array[1::2,:]
        reference_off_array = reference_array[::2,:]

	#"def average_shots"
	##############################################################################
	
    probe_on = probe_on_array.mean(axis=0)
    probe_off = probe_off_array.mean(axis=0)
    reference_on = reference_on_array.mean(axis=0)
    reference_off = reference_off_array.mean(axis=0)
    
    print ("Pump", probe_on)
    print ("Probe", probe_off)
	
	#Stop connection
	##############################################################################
	##############################################################################

    c_lib.USB3_RequeueBuffer.argtypes = [c_void_p, c_void_p]
    c_lib.USB3_RequeueBuffer.restype = None    
    c_lib.USB3_RequeueBuffer(hCamera, ImageInfos.hBuffer)

    c_lib.USB3_StopAcquisition(hCamera)

    c_lib.USB3_FlushBuffers(hCamera)

    c_lib.USB3_CloseCamera(hCamera)

    c_lib.USB3_TerminateLibrary()

    print("Complete")


else:
    print("Error")
	
