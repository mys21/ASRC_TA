from aerodiode import Tombak
from math imput ceil


class Tombak_control():
    def __init__(self):
        self.frame_freq = 1 # read from tombak
        self.line_freq = 1  # read from tombak
        self.line_port = 'COM5' 
        self.frame_port = 'COM3'
        self.voltage = 0.5 # units of V
        self.line_pulse_width = 260 # units of ns
        self.frame_pulse_width = 800 # units of ns
        self.line_pulse_delay = 975000 # units of 100 ps
        self.frame_pulse_delay = 111100 # units of 100 ps
  
    def line_parameters(self):
        tombak = Tombak(self.line_port)
        self.line_freq = tombak.measure_pulse_in_frequency()
        tombak.set_integer_instruction(tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV, 1)
        tombak.set_voltage_instruction(tombak.INSTRUCT_PULSE_IN_THRESHOLD, self.voltage) # units V
        tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, self.line_pulse_width) # units ns
        tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY, self.line_pulse_delay) # units 100ps
        tombak.apply_all()
        del(tombak)
        return

    def frame_parameters(self,num_shots):
        tombak = Tombak(self.frame_port)
        self.frame_freq = tombak.measure_pulse_in_frequency()
        self.division = ceil(self.frame_freq / (self.line_freq / num_shots))
        tombak.set_integer_instruction(tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV, int(self.division))	# num_shots/3
        tombak.set_voltage_instruction(tombak.INSTRUCT_PULSE_IN_THRESHOLD, self.voltage) # units V
        tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, self.frame_pulse_width) # units ns
        tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY, self.frame_pulse_delay) # units 100ps
        tombak.apply_all()
        #print("INSTRUCT_PULSE_OUT_DELAY = ",tombak.read_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY))
        del(tombak)
        return
    
    def Initialize_tombak(self,num_shots):
        self.line_parameters()
        self.frame_parameters(num_shots)
        return
