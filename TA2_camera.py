from ctypes import *
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class tCameraInfo(Structure):
	_fields_ = [("pcID", c_char*260)]

class octoplus(QObject):
    def __init__(self):
        super(QObject,self).__init__()        
        #self.dll = ct.WinDLL(r"E:\Installation files\CD copy - InGaAs photodiode arrays\ESLSCDLL\Release\ESLSCDLL.dll")
        self.dll = ct.WinDLL(r"C:\Users\mysfe\OneDrive\Desktop\ASRC_TA\CamCmosOctUsb3.dll")
        self.pixels = 2048 #including dummy pixels
        self.num_pixels = 2048
        self.first_pixel = 0
        self.enable_contextual_data = 1
		self.circular_buffer = 1
		self.trigger_mode = 4
		self.exposure_time = 132 # units of 10 ns 
		self.max_bulk_queue_number = 16
		self.timeout = c_ulong(3000)
		self.iNbOfBuffer = c_size_t(30)
		self.ulNbCameras = c_ulong()
        
    #Combined Methods to Call Camera Easily
    def Initialize(self,lines_per_frame=45000):
        self.lines_per_frame = lines_per_frame
        InitializeLibrary()

        ulNbCameras= c_ulong()
        #c_lib.USB3_UpdateCameraList.restype = c_ulong
        c_lib.USB3_UpdateCameraList(byref(ulNbCameras))
        #print('Number of Cameras: ',ulNbCameras.value)	#Works
 
        ulIndex= c_ulong(0) 
        CameraInfo = tCameraInfo()
        c_lib.USB3_GetCameraInfo.restype = c_char*260 #this variable type should actually be tCameraInfo.... - char array type? #changed output to c_char*260 instead of tCameraInfo, this change allowed us to make changes to the camera register.
        USB3_GetCameraInfo(ulIndex,byref(CameraInfo))  #'CameraInfo = ' removed
        #print("Camera ID: ", CameraInfo.pcID)	#prints memory location, try to print the values of the char array

        hCamera=c_void_p()
        c_lib.USB3_OpenCamera.restype = c_void_p
        c_lib.USB3_OpenCamera(byref(CameraInfo), byref(hCamera))  #byref(hCamera.pointer)

        c_lib.USB3_WriteRegister.restype = c_size_t
        ulAddress= c_ulong(0x4F000000) 
        ulValue = c_ulong(1)  #contextual data on or off
        iSize = c_size_t(ulValue.__sizeof__())
        WriteRegister = c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
        print('Enable contextual data: ', ulValue.value)

        ulAddress= c_ulong(0x4F000018) 
        ulValue = c_ulong(0)  #circular buffer on or off
        c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
        print('Circular buffer: ', ulValue.value)

	    ulAddress= c_ulong(0x1210C) 
        ulValue = c_ulong(4)  #trigger mode
        c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
        print('Trigger mode: ', ulValue.value)

        ulAddress= c_ulong(0x12108) 
        ulValue = c_ulong(132)  #exposure time
        c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
        print('Exposure time: ', ulValue.value)

        ulAddress= c_ulong(0x4F000010) 
        ulValue = c_ulong(16)  #max bulk queue number
        c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
        print('Max bulk queue number: ', ulValue.value)

        ulAddress= c_ulong(0x12128) 
        ulValue = c_ulong(45000)  #lines per frame
        c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
        print('Lines per frame: ', ulValue.value)

        ulAddress= c_ulong(0x12100) 
        ulValue = c_ulong(1111)  #line period x 10^(-8) seconds
        c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
        print('Line period: ', ulValue.value)

        ulAddress= c_ulong(0x1211C) 
        ulValue = c_ulong(80)  #pulse width discriminator x 10^(-8) seconds
        c_lib.USB3_WriteRegister(hCamera, ulAddress, byref(ulValue), byref(iSize))
        print('Pulse width: ', ulValue.value)

        iImageHeight = c_size_t(45000)
        iNbOfBuffer = c_size_t(30)

        #c_lib.USB3_SetImageParameters.restype = None
        c_lib.USB3_SetImageParameters(hCamera, iImageHeight, iNbOfBuffer)
        self.array = np.zeros((self.number_of_scans+10,self.pixels*2),dtype=np.dtype(np.int16))
        self.data = self.array[10:]
        self.Wait(300000)
        return 
        
    def Wait(self,time_us):
        self.InitSysTimer()
        tick_start = self.TicksTimestamp()
        time_start = self.Tickstous(tick_start)
        tick_end = self.TicksTimestamp()
        time_end = self.Tickstous(tick_end)
        while (time_end - time_start) < time_us:
            tick_end = self.TicksTimestamp()
            time_end = self.Tickstous(tick_end)
        return
    
    start_acquire = pyqtSignal()
    data_ready = pyqtSignal(np.ndarray,np.ndarray,int,int)
    @pyqtSlot()
    def Acquire(self):
        self.ReadFFLoop(self.number_of_scans,self.exposure_time_us)
        self.Construct_Data_Vec()
        self.data_ready.emit(self.probe,self.reference,self.first_pixel,self.num_pixels)
        return 
        
    def Construct_Data(self):
        hi = np.zeros(self.data[0].shape)
        lo = np.zeros(self.data[0].shape)
        self.probe = np.zeros((len(self.data),self.pixels))
        self.reference = np.zeros((len(self.data),self.pixels))
        for i,shot in enumerate(self.data):
            for j,value in enumerate(shot):
                hi[j] = value >> 16
                lo[j] = value & 0xffff
            interleaved_shot = np.empty((hi.size+lo.size,), dtype=hi.dtype)
            interleaved_shot[0::2] = hi
            interleaved_shot[1::2] = lo
            self.probe[i] = interleaved_shot[0:self.pixels]
            self.reference[i] = interleaved_shot[self.pixels:self.pixels*2]
        return
        
    def Construct_Data_Vec(self):
        # dtype of self.data is uint32
        self.probe = self.data.view(np.uint16)[:,0:self.pixels*2]  # temp = shots x (2*pixels)
        # either:        
        #d = hiloArray.shape;
        #self.probe     = hiloArray[:,0:(d[-1]/2)]
        #self.reference = hiloArray[:,(d[-1]/2+1):d[-1]]
        # or: (easier to read)
        hiloArray = hiloArray.reshape(hiloArray.shape[0],2,self.pixels)
        self.probe     = hiloArray[:,0,:]       # pointers onto self.data
        self.reference = hiloArray[:,1,:]
    
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

	def UpdateCameraList(self, pulNbCameras)):
	    self.dll.USB3_UpdateCameraList.restype = c_ulong
		self.dll.USB3_UpdateCameraList(pulNbCameras)

	def GetCameraInfo(self, ulIndex, pCameraInfo):
	    self.dll.USB3_GetCameraInfo.restype = c_char*260
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



    def AboutDrv(self):
        self.dll.DLLAboutDrv(ct.c_uint32(self.board_number))
        
    def ActCooling(self):
        self.dll.DLLActCooling(ct.c_uint32(self.board_number),
                               ct.c_uint8(1))
                               
    def ActMouse(self):
        self.dll.DLLActMouse(ct.c_uint32(self.board_number))
    
    def Cal16bit(self):
        self.dll.DLLCal16Bit(ct.c_uint32(self.board_number),
                              ct.c_uint32(self.zadr))

    def CCDDrvExit(self):
        self.dll.DLLCCDDrvExit(ct.c_uint32(self.board_number))
        
    def CCDDrvInit(self):
        found = self.dll.DLLCCDDrvInit(ct.c_uint32(self.board_number))
        return bool(found)
        
    def CloseShutter(self):
        self.dll.DLLCloseShutter(ct.c_uint32(self.board_number))
        
    def ClrRead(self,clr_count):
        self.dll.DLLClrRead(ct.c_uint32(self.board_number),
                            ct.c_uint32(self.fft_lines),
                            ct.c_uint32(self.zadr),
                            ct.c_uint32(clr_count))
                            
    def ClrShCam(self):
        self.dll.DLLClrShCam(ct.c_uint32(self.board_number),
                             ct.c_uint32(self.zadr))
    
    def DeactMouse(self):
        self.dll.DLLDeactMouse(ct.c_uint32(self.board_number))
    
    def DisableFifo(self):
        self.dll.DLLDisableFifo(ct.c_uint32(self.board_number))
        
    def EnableFifo(self):
        self.dll.DLLEnableFifo(ct.c_uint32(self.board_number))
    
    def FFOvl(self):
        overflow = self.dll.DLLFFOvl(ct.c_uint32(self.board_number))
        return bool(overflow)
        
    def FFValid(self):
        valid = self.dll.DLLFFValid(ct.c_uint32(self.board_number))
        return bool(valid)
        
    def FFRS(self):
        self.dll.DLLRSFifo(ct.c_uint32(self.board_number))
        
    def FlagXCKI(self):
        active = self.dll.DLLFlagXCKI(ct.c_uint32(self.board_number))
        return bool(active)
        
    def GetCCD(self):
        self.dll.DLLGETCCD(ct.c_uint32(self.board_number),
                           self.array.ctypes.data,
                           ct.c_uint32(self.fft_lines),
                           ct.c_uint32(self.fkt),
                           ct.c_uint32(self.zadr))
        return self.array
        
    def HighSlope(self):
        self.dll.DLLHighSlope(ct.c_uint32(self.board_number))
     
    def InitBoard(self):
        self.dll.DLLInitBoard(ct.c_uint32(self.board_number),
                              ct.c_int8(self.sym),
                              ct.c_uint8(self.burst),
                              ct.c_uint32(self.pixels),
                              ct.c_uint32(self.waits),
                              ct.c_uint32(self.flag816),
                              ct.c_uint32(self.pportadr),
                              ct.c_uint32(self.pclk),
                              ct.c_uint32(self.adrdelay))
        
    def InitGPX(self):
        self.dll.DLLInitGPX(ct.c_uint32(self.board_number),
                            ct.c_ulong(self.startoffset))
        
    def InitSysTimer(self):
        return self.dll.DLLInitSysTimer()
        
    def LowSlope(self):
        self.dll.DLLLowSlope(ct.c_uint32(self.board_number))
    
    def OpenShutter(self):
        self.dll.DLLOpenShutter(ct.c_uint32(self.board_number))
    
    def OutTrigHigh(self):
        self.dll.DLLOutTrigHigh(ct.c_uint32(self.board_number))
        
    def OutTrigLow(self):
        self.dll.DLLOutTrigLow(ct.c_uint32(self.board_number))
    
    def OutTrigPulse(self,pulse_width):
        self.dll.DLLOutTrigPulse(ct.c_uint32(self.board_number),
                                 ct.c_uint32(pulse_width))
    
    def ReadFifo(self):
        self.dll.DLLReadFifo(ct.c_uint32(self.board_number),
                             self.array.ctypes.data,
                             ct.c_uint32(self.fkt))
        return self.array
    
    def ReadFFCounter(self):
        counter = self.dll.DLLReadFFCounter(ct.c_uint32(self.board_number))
        return counter        
    
    def ReadFFLoop(self,number_of_scans,exposure_time_us):
        self.dll.DLLReadFFLoop(ct.c_uint32(self.board_number),
                               self.array.ctypes.data,
                               ct.c_uint32(self.fft_lines),
                               ct.c_int32(self.fkt),
                               ct.c_uint32(self.zadr),
                               ct.c_uint32(number_of_scans+10),
                               ct.c_uint32(exposure_time_us),
                               ct.c_uint32(self.freq),
                               ct.c_uint32(self.threadp),
                               ct.c_uint32(self.clear_cnt),
                               ct.c_uint16(self.release_ms),
                               ct.c_uint8(self.exttrig),
                               ct.c_uint8(self.block_trigger))
                               
    def RSFifo(self):
        self.dll.DLLRSFifo(ct.c_uint32(self.board_number))
        
    def RsTOREG(self):
        self.dll.DLLRsTOREG(ct.c_uint32(self.board_number))
        
    def SetADAmpRed(self,gain):
        self.dll.DLLSetADAmpRed(ct.c_uint32(self.board_number),
                                ct.c_uint32(gain))
    
    def SetAD16Default(self):
        self.dll.DLLSetAD16Default(ct.c_uint32(self.board_number),
                                   ct.c_uint32(1))
                                   
    def SetExtTrig(self):
        self.dll.DLLSetExtTrig(ct.c_uint32(self.board_number))
        
    def StopFFTimer(self):
        self.dll.DLLStopFFTimer(ct.c_uint32(self.board_number))
        
    def SetIntTrig(self):
        self.dll.DLLSetIntTrig(ct.c_uint32(self.board_number))
        
    def SetISFFT(self,_set):
        self.dll.DLLSetISFFT(ct.c_uint32(self.board_number),
                             ct.c_uint8(_set))
    
    def SetISPDA(self,_set):
        self.dll.DLLSetISPDA(ct.c_uint32(self.board_number),
                             ct.c_uint8(_set))
                             
    def SetOvsmpl(self):
        self.dll.DLLSetOvsmpl(ct.c_uint32(self.board_number),
                              ct.c_uint32(self.zadr))
    
    def SetTemp(self,level):
        self.dll.DLLSetTemp(ct.c_uint32(self.board_number),
                            ct.c_uint32(level))
    
    def SetupDelay(self,delay):
        self.dll.DLLSetupDELAY(ct.c_uint32(self.board_number),
                               ct.c_uint32(delay))
    
    def SetupHAModule(self,fft_lines):
        self.dll.DLLSetupHAModule(ct.c_uint32(self.board_number),
                                  ct.c_uint32(fft_lines))
    
    def StartTimer(self,exposure_time):
        self.dll.DLLStartTimer(ct.c_uint32(self.board_number),
                               ct.c_uint32(exposure_time))
    
    def TempGood(self,channel):
        self.dll.DLLTempGood(ct.c_uint32(self.board_number),
                             ct.c_uint32(channel))
                             
    def TicksTimestamp(self):
        ticks = self.dll.DLLTicksTimestamp()
        return ticks
        
    def Tickstous(self,ticks):
        us = self.dll.DLLTickstous(ct.c_uint64(ticks))
        return us
    
    def Von(self):
        self.dll.DLLVOn(ct.c_uint32(self.board_number))
        
    def Voff(self):
        self.dll.DLLVOff(ct.c_uint32(self.board_number))
        
    def WaitforTelapsed(self,t_us):
        success = self.dll.DLLWaitforTelapsed(ct.c_uint32(t_us))
        return bool(success)
        
    def WriteL(self,databyte,portoff):
        self.dll.DLLWriteLongS0(ct.c_uint32(self.board_number),ct.c_uint32(databyte),ct.c_uint32(portoff))
                           