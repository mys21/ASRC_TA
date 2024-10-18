from aerodiode import Tombak
from math import ceil


class Tombak_control:
    def __init__(self):
        self.frame_freq = 1 # read from tombak
        self.line_freq = 1  # read from tombak
        self.line_port = 'COM5' 
        self.frame_port = 'COM3'
        self.frame_voltage = 1 # units of V
        self.line_voltage = 0.5 # units of V
        self.line_pulse_width = 260 # units of ns
        self.frame_pulse_width = 800 # units of ns
        self.line_pulse_delay =	97500         # units of 100 ps (default for 90kHz)
        self.frame_pulse_delay = 111100 #1000000 # units of 100 ps
        self.nDivTom = 900		# division from tombak 1
        self.division = 1
        self.switch = False
 

  
    def line_parameters(self):
        tombak = Tombak(self.line_port)
        #tombak.set_status_instruction(tombak.INSTRUCT_FUNCTIONING_MODE, 0) # does this work??
        tombak.set_voltage_instruction(tombak.INSTRUCT_PULSE_IN_THRESHOLD, self.line_voltage) # units V
        self.line_freq = tombak.measure_pulse_in_frequency()
        self.line_pulse_delay = int((1/self.line_freq - 1.6e-6)/1e-10)
        tombak.set_integer_instruction(tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV, 1)
        tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, self.line_pulse_width) # units ns
        tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY, self.line_pulse_delay) # units 100ps
        tombak.set_status_instruction(tombak.INSTRUCT_SYNC_OUT_2_SOURCE, 0)	# "source synchro 2: input"
        #tombak.set_status_instruction(tombak.INSTRUCT_SYNC_OUT_1_SOURCE, 3)	# "source synchro 1: pulse"
        tombak.apply_all()
        #print("Line INSTRUCT_PULSE_OUT_DELAY =", tombak.read_status_instruction(tombak.INSTRUCT_SYNC_OUT_2_SOURCE))
        del(tombak)
        return

    def frame_parameters(self,num_shots):
        tombak = Tombak(self.frame_port)
        #tombak.set_status_instruction(tombak.INSTRUCT_FUNCTIONING_MODE, ON) # does this work??
        tombak.set_voltage_instruction(tombak.INSTRUCT_PULSE_IN_THRESHOLD, self.frame_voltage) # units V
        self.frame_freq = tombak.measure_pulse_in_frequency()
        #self.division = ceil(self.frame_freq / (self.line_freq / num_shots))
        self.division = ceil(num_shots/self.nDivTom) # div by 3 method use: ceil(1/3*num_shots) # should have the same division as the pump pulse for the laser
        tombak.set_integer_instruction(tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV,self.division)	# num_shots/4
        tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, self.frame_pulse_width) # units ns
        tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY, self.frame_pulse_delay) # units 100ps
        tombak.set_status_instruction(tombak.INSTRUCT_SYNC_OUT_2_SOURCE, 1)	#IR camera - "source synchro 2: output"
        tombak.apply_all()
        #print("Frame INSTRUCT_PULSE_OUT_DELAY =", tombak.read_status_instruction(tombak.INSTRUCT_SYNC_OUT_2_SOURCE))
        #print("INSTRUCT_PULSE_OUT_DELAY = ",tombak.read_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY))
        del(tombak)
        return
    
    def Initialize_tombak(self,num_shots):
        self.line_parameters()
        self.frame_parameters(num_shots)
        return

    def Rep_rate_check(self):
        if Tombak(self.line_port).measure_pulse_in_frequency() < 90000:
            self.switch = True
        return self.switch
