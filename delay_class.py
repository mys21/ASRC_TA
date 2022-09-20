#from PyAPT import APTMotor
#from XPS_C8_drivers import XPS
#import visa
#import serial
import time as pytime
# Add ESP301 specific code
import sys
# requires pythonnet module for C# dll (tested with 2.5?)
import clr
import System
from System import UInt32, Int32
from System import Double
import scipy.constants as spc
#here or above?
sys.path.append(r'C:\Windows\Microsoft.NET\assembly\GAC_64\Newport.ESP301.CommandInterface\v4.0_2.0.0.3__9f994642f5b48132')
clr.AddReference("Newport.ESP301.CommandInterface")
from CommandInterfaceESP301 import *
        
class thorlabs_delay_stage:
    def __init__(self,t0):
        self.stage = APTMotor(94862873,HWTYPE=44)
        self.stage.initializeHardwareDevice()
        self.t0 = t0
        self.initialized=True
    
    def home(self):
        self.stage.go_home()
        return
        
    def move_to(self,time_point_ps):
        new_pos_mm = self.convert_ps_to_mm(float(self.t0-time_point_ps))
        self.stage.mcAbs(new_pos_mm,moveVel=50)
        return False
        
    def convert_ps_to_mm(self,time_ps):
        pos_mm = 0.29979*time_ps/2
        return pos_mm
        
    def close(self):
        self.stage.cleanUpAPT()
        return
        
    def check_times(self,times):
        all_on_stage = True
        for time in times:
            pos = self.convert_ps_to_mm(float(self.t0-time))
            if (pos>300) or (pos<0):
                all_on_stage = False
        return all_on_stage
        
    def check_time(self,time):
        on_stage = True
        pos = self.convert_ps_to_mm(float(self.t0-time))
        if (pos>300) or (pos<0):
            on_stage = False
        return on_stage

class esp301_delay_stage:
    def __init__(self,t0):
        self.t0 = t0
        self.passes = 2
        self.axis = Int32(1)
        self.instrument="COM4"
        self.BAUDRATE=921600

        # create an ESP301 instance
        # add print statement for intialization!!!
        self.stage = ESP301()
        ret = self.stage.OpenInstrument(self.instrument, self.BAUDRATE); 
        if ret == 0:
            self.initialized=True
            print("Delay Stage Initialized")
        else:
            print("Delay Stage Error!")
            self.initialized=False
        # Initialize motor
        result, errString = self.stage.MO_Set(self.axis,"")
        # Get positive software limit
        result, rlimit, errString = self.stage.SR_Get(self.axis,Double(0.),"")
        self.plimit = rlimit
        # Get negative software limit
        result, llimit, errString = self.stage.SL_Get(self.axis,Double(0.),"")
        self.nlimit = llimit
        #home stage to reset all
        #self.home()

    def home(self):
        result, errString = self.stage.OR(self.axis,Int32(0),"")
        response = 0
        while response == 0:
            pytime.sleep(.5)
            result2, response, errString2 = self.stage.MD(self.axis,Int32(1),"")
        return
   
    def move_to(self,time_point_ps):
        # why is this self.t0-time_point_ps --> front of the stage is max travel, so moving to smaller positions?
        #new_pos_mm = self.convert_ps_to_mm(float(self.t0-time_point_ps))
        # I think our stage is the other way (front is lower limit) --> need to double check
        new_pos_mm = self.convert_ps_to_mm(float(self.t0+time_point_ps))
        result, errString = self.stage.PA_Set(self.axis, Double(new_pos_mm),"")
        response = 0
        while response == 0:
            pytime.sleep(.1)
            result2, response, errString2 = self.stage.MD(self.axis,Int32(1),"")
        #print([errString, result2])
        result, currentPosition, errString = self.stage.TP(self.axis, Double(0.), "")
        #print([errString, currentPosition])
        return

    def convert_ps_to_mm(self,time_ps):
        # account for 2 pass configuration
        # stage is referenced to middle
        pos_mm = self.nlimit + 0.29979*time_ps/(2*self.passes)
        return pos_mm

    def close(self):
        self.stage.CloseInstrument(); 

    def check_times(self,times):
        all_on_stage = True
        # change to read stage limits
        # original code limits differ from check_time
        for time in times:
            #pos = self.convert_ps_to_mm(float(self.t0-time))
            pos = self.convert_ps_to_mm(float(self.t0+time))
            if (pos>self.plimit) or (pos<self.nlimit):
            #if (pos>300) or (pos<-300):
                all_on_stage = False
        return all_on_stage

    def check_time(self,time):
        on_stage = True
        #pos = self.convert_ps_to_mm(float(self.t0-time))
        pos = self.convert_ps_to_mm(float(self.t0+time))
        #print(pos)
        # change to read stage limits
        if (pos>self.plimit) or (pos<self.nlimit):
        #if (pos>300) or (pos<-300):
            on_stage = False
        return on_stage

    def get_posmm(self):
        result, currentPosition, errString = self.stage.TP(self.axis, Double(0.), "")
        if result == 0 :
            print('position=>', currentPosition)
        else:
            print('Error=>',errString)
        return currentPosition

class newport_delay_stage:
    def __init__(self,t0):
        self.t0 = t0
        self.stage = XPS()
        self.group = 'GROUP1'
        self.positioner = self.group+'.POSITIONER'
        self.socketId = self.stage.TCP_ConnectToServer('192.168.0.254', 5001, 20)
        [errorCode, returnString] = self.stage.GroupInitialize(self.socketId,self.group)
        print([errorCode, returnString])
        if errorCode != 0:
            self.stage.GroupKill(self.socketId,self.group)
            [errorCode, returnString] = self.stage.GroupInitialize(self.socketId,self.group)
            self.stage.GroupHomeSearch(self.socketId,self.group)
        if errorCode !=0:
            self.initialized=False
        if errorCode ==0:
            self.initialized=True
        
    def home(self):
        [errorCode, returnString] = self.stage.GroupHomeSearch(self.socketId,self.group)
        return
        
    def move_to(self,time_point_ps):
        new_pos_mm = self.convert_ps_to_mm(float(self.t0-time_point_ps))
        [errorCode, returnString] = self.stage.GroupMoveAbsolute(self.socketId,self.positioner, [new_pos_mm])
        print([errorCode, returnString])
        [errorCode, currentPosition] = self.stage.GroupPositionCurrentGet(self.socketId,self.positioner, 1)
        print([errorCode, currentPosition])
        return
        
    def convert_ps_to_mm(self,time_ps):
        pos_mm = 0.29979*time_ps/2
        return pos_mm
        
    def close(self):
        self.stage.TCP_CloseSocket(self.socketId) 
        
    def check_times(self,times):
        all_on_stage = True
        for time in times:
            pos = self.convert_ps_to_mm(float(self.t0-time))
            if (pos>279) or (pos<0):
                all_on_stage = False
        return all_on_stage
        
    def check_time(self,time):
        on_stage = True
        pos = self.convert_ps_to_mm(float(self.t0-time))
        if (pos>300) or (pos<0):
            on_stage = False
        return on_stage
        
class pink_laser_delay:
    def __init__(self,t0):
        self.gen_gpib_address = 'GPIB::15::INSTR'
        self.rm = visa.ResourceManager()
        self.gen = self.rm.open_resource(self.gen_gpib_address)
        self.t0 = t0
        self.initialized=True
        
    def move_to(self,time_point_ns):
        tau_flip_request = False
        new_time = (self.t0-time_point_ns)*1E-9
        if new_time < 0:
            tau_flip_request = True
            new_time = new_time + 0.001
        time_point_string = '%.5e' % (new_time)
        self.gen.write('DT 2,1,'+time_point_string)
        return tau_flip_request
        
        
    def check_times(self,times):
        all_between_two_shots = True
        for time in times:
            new_time = (self.t0-time)*1E-9
            if (new_time<-0.001) or (new_time>0.001):
                all_between_two_shots = False
        return all_between_two_shots
        
    def check_time(self,time):
        between_two_shots = True
        new_time = (self.t0-time)*1E-9
        if (new_time<-0.001) or (new_time>0.001):
            between_two_shots = False
        return between_two_shots
    
class disco_laser_delay:
        
    def __init__(self,t0,port,baud):
        
        self.ser = serial.Serial(port, baud, timeout=1)
        self.t0 = t0
        if self.ser.isOpen():
            self.initialized=True
        else:
            self.initialized=False
        cmd = ('tl 1; tr po; tr te; td 0; aw 10n; as po; as on \r\n').encode('UTF-8')
        self.ser.write(cmd)
            
    def close(self):
        self.ser.close() 

#==============================================================================
#     def move_to(self,time_point_ns):
#         tau_flip_request = False
#         new_time = (self.t0+time_point_ns)*1E-9
#         if new_time > 0:
#             A_new = new_time
#             B_new = 465*1E-6
#             C_new = new_time+(3*1E-6)
#             D_new = 500*1E-6
#             AB_pol = 0
#             CD_pol = 1
#         elif new_time < -0.000003:
#            new_time_abs = -new_time
#            A_new = 465E-6-new_time_abs
#            B_new = 534.85*1E-6
#            C_new = 503E-6-new_time_abs
#            D_new = 500*1E-6
#            AB_pol = 1
#            CD_pol = 0
#         else:   
#            new_time_abs = -new_time
#            A_new = 465*1E-6 - new_time_abs
#            B_new = 534.85*1E-6
#            C_new = 3*1E-6 - new_time_abs
#            D_new = 500*1E-6
#            AB_pol = 1
#            CD_pol = 1    
#            #tau_flip_request = True
#            #new_time = new_time + 0.001  
#         A_new_string = '%.5e' % (A_new)    
#         B_new_string = '%.5e' % (B_new)
#         C_new_string = '%.5e' % (C_new)
#         D_new_string = '%.5e' % (D_new)
#         AB_pol_string = '%d' % (AB_pol)
#         CD_pol_string = '%d' % (CD_pol)
#         self.gen.write('IFRS 1')
#         self.gen.write('DT 2,1,'+A_new_string)
#         self.gen.write('IFRS 1')
#         self.gen.write('DT 3,2,'+B_new_string)
#         self.gen.write('IFRS 1')
#         self.gen.write('DT 5,1,'+C_new_string)
#         self.gen.write('IFRS 1')
#         self.gen.write('DT 6,5,'+D_new_string)
#         self.gen.write('IFRS 1')
#         self.gen.write('LPOL 1,'+AB_pol_string)
#         self.gen.write('IFRS 1')
#         self.gen.write('LPOL 2,'+CD_pol_string)
#         return tau_flip_request
#==============================================================================
    
    def move_to(self,time_point_ns):
        tau_flip_request = False
        new_time_ns = (self.t0+time_point_ns)
        cmd = ('ad ' + str(new_time_ns) +'n \r\n').encode('UTF-8')
        self.ser.write(cmd)
        self.DG_out = ''
        self.DG_output_state=False
        # let's wait before reading output (let's give device time to answer)
        pytime.sleep(0.05)
        self.DG_out += self.ser.read(100).decode('ascii')
        if self.DG_out != '':
            self.DG_output_state=True
        return tau_flip_request

    
    def check_times(self,times):
        all_between_two_shots = True
        for time in times:
            new_time_ns = (self.t0+time)
            if (new_time_ns<0) or (new_time_ns>1E6):
                all_between_two_shots = False
        return all_between_two_shots
        
    def check_time(self,time):
        between_two_shots = True
        new_time_ns = (self.t0+time)
        if (new_time_ns<0) or (new_time_ns>1E6):
            between_two_shots = False
        return between_two_shots
