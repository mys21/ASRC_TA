from aerodiode import Tombak
#from time import time

class tombak(Object):
    def __init__(self):
    

def Tombak_frame_initialise(num_shots):
    tombak = Tombak('COM3')
    frame_freq = tombak.measure_pulse_in_frequency()
    print("INSTRUCT_PULSE_IN_SRC = ", frame_freq, " Hz")
    division = frame_freq / (90000 / num_shots)
    tombak.set_integer_instruction(tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV, int(division))	# num_shots/3
    tombak.set_voltage_instruction(tombak.INSTRUCT_PULSE_IN_THRESHOLD, 0.5) # units V
    tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, 800) # units ns
    tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY, 111100) # units 100ps
    tombak.apply_all()
    #print("INSTRUCT_PULSE_OUT_DELAY = ",tombak.read_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY))
    del(tombak)
    return

def Tombak_line_initialise():
    tombak = Tombak('COM5')
    line_freq = tombak.measure_pulse_in_frequency()
    tombak.set_integer_instruction(tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV, 1)
    tombak.set_voltage_instruction(tombak.INSTRUCT_PULSE_IN_THRESHOLD, 0.5) # units V
    tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, 260) # units ns
    tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY, 975000) # units 100ps
    tombak.apply_all()
    del(tombak)
    return


#Tombak_initialise(45000, 'COM3')
