#main Tombak

NULL = "csv_png/tombak/rectangle_500_pts_0A.csv"
RECTANGLE = "csv_png/tombak/rectangle_10_pts_1A.csv"
RECTANGLE2 = "csv_png/tombak/rectangle_200_pts_1A.csv"
TRIANGLE  = "csv_png/tombak/triangle_10_pts_1A.csv"
BATMAN    = "csv_png/tombak/batman.csv"
SHAPE_MAX = "csv_png/tombak/shape_max.csv"

from tombak import Tombak

tombak = Tombak('COM9')
tombak.set_integer_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, 2E64-1)
tombak.apply_all()
res = int(input("Do you prefer (tap 1 or 2) :\n1.Standalone\n2.Digital Delay Generator\n3.AWG (Arbitrary Waveform Generator)\n"))


if (res == 1):
    print("Set Configuration")
    tombak.set_status_instruction(tombak.INSTRUCT_PULSE_IN_SRC, tombak.DIRECT)
    tombak.set_status_instruction(tombak.INSTRUCT_TRIGGER_SRC, tombak.INT)
    tombak.set_status_instruction(tombak.INSTRUCT_SYNC_OUT_1_SRC, tombak.PULSE_OUT)
    tombak.set_status_instruction(tombak.INSTRUCT_GATE_CONTROL, tombak.NO_GATE)
    tombak.set_freq_instruction(tombak.INSTRUCT_INTERN_TRIGGER_FREQ, 100000)
    tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, 5)
    tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY, 0)

    divider = int(input("Tap divider value :"))
    tombak.set_integer_instruction(tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV, divider)
    
    output_frequency = tombak.PULSE_FREQ/divider
    print("output frequency =", output_frequency)
    
    duty_cycle = float(input("Tap duty cycle (en %) :"))
    pulse_width = (duty_cycle/(100*output_frequency)*1000000000) #pb
    print("pulse width = ", pulse_width)
    tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, int(pulse_width))
    tombak.apply_all()


    print("Read Configuration")
    print("INSTRUCT_FUNCTIONING_MODE = ", tombak.read_status_instruction(tombak.INSTRUCT_FUNCTIONING_MODE))
    print("INSTRUCT_PULSE_IN_SRC = ", tombak.read_status_instruction(tombak.INSTRUCT_PULSE_IN_SRC))
    print("INSTRUCT_PULSE_IN_FREQUENCY_DIV = ", tombak.read_freq_instruction(tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV))
    print("INSTRUCT_SYNC_OUT_1_SRC = ", tombak.read_status_instruction(tombak.INSTRUCT_SYNC_OUT_1_SRC))
    print("INSTRUCT_PULSE_OUT_WIDTH = ", tombak.read_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH))

elif (res == 2):
    print("Set Configuration")
    tombak.set_status_instruction(tombak.INSTRUCT_FUNCTIONING_MODE, tombak.PULSE_PICKER)
    tombak.set_status_instruction(tombak.INSTRUCT_PULSE_IN_SRC, tombak.DIRECT)#ok
    tombak.set_status_instruction(tombak.INSTRUCT_TRIGGER_SRC, tombak.INT)#
    tombak.set_status_instruction(tombak.INSTRUCT_SYNC_OUT_1_SRC, tombak.PULSE_OUT)#ok
    tombak.set_status_instruction(tombak.INSTRUCT_GATE_CONTROL, tombak.NO_GATE)#ok
    tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, 100)#ok
    tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY, 100)#ok
    print("\n")
    print("Read New Configuration")
    print("INSTRUCT_FUNCTIONING_MODE = ", tombak.read_status_instruction(tombak.INSTRUCT_FUNCTIONING_MODE))
    print("INSTRUCT_PULSE_IN_SRC = ", tombak.read_status_instruction(tombak.INSTRUCT_PULSE_IN_SRC))#ok
    print("INSTRUCT_TRIGGER_SRC = ", tombak.read_status_instruction(tombak.INSTRUCT_TRIGGER_SRC))#
    print("INSTRUCT_SYNC_OUT_1_SRC = ", tombak.read_status_instruction(tombak.INSTRUCT_SYNC_OUT_1_SRC))#ok
    print("INSTRUCT_GATE_CONTROL = ", tombak.read_status_instruction(tombak.INSTRUCT_GATE_CONTROL))#ok
    print("INSTRUCT_PULSE_OUT_WIDTH = ", tombak.read_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH))#ok
    print("INSTRUCT_PULSE_OUT_DELAY = ", tombak.read_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY))#ok
    print("\n")
    print("Measurement")
    print("pulse in frequency = ", tombak.measure_pulse_in_frequency())

    
    
    


elif (res == 3):
    print("Set Configuration")
    
    tombak.set_status_instruction(tombak.INSTRUCT_FUNCTIONING_MODE, tombak.PULSE_SHAPE_GENERATOR)
    tombak.set_status_instruction(tombak.INSTRUCT_PULSE_IN_SRC, tombak.DIRECT)
    tombak.set_status_instruction(tombak.INSTRUCT_TRIGGER_SRC, tombak.INT)
    tombak.set_status_instruction(tombak.INSTRUCT_SYNC_OUT_1_SRC, tombak.PULSE_OUT)
    tombak.set_status_instruction(tombak.INSTRUCT_GATE_CONTROL, tombak.NO_GATE)
    tombak.set_freq_instruction(tombak.INSTRUCT_INTERN_TRIGGER_FREQ, 100000)
    tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, 5)
    tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY, 0)
    

    print("Set SHAPE Configuration")
    csv_table = tombak.read_csv(SHAPE_MAX)
    tombak.set_integer_instruction(tombak.INSTRUCT_SHAPE1_STEP_NUMBER, csv_table[0])
    tombak.set_integer_instruction(tombak.INSTRUCT_SHAPE1_STEP_SIZE) 
    tombak.send_csv(0x00, csv_table)
    tombak.save_shape_data()
    tombak.apply_all()

    print("Read Configuration")
    print("INSTRUCT_FUNCTIONING_MODE = ",tombak.read_status_instruction(tombak.INSTRUCT_FUNCTIONING_MODE))
    print("INSTRUCT_PULSE_IN_SRC, = ",tombak.read_status_instruction(tombak.INSTRUCT_PULSE_IN_SRC))
    print("INSTRUCT_TRIGGER_SRC = ",tombak.read_status_instruction(tombak.INSTRUCT_TRIGGER_SRC))
    print("INSTRUCT_SYNC_OUT_1_SRC = ",tombak.read_status_instruction(tombak.INSTRUCT_SYNC_OUT_1_SRC))
    print("INSTRUCT_GATE_CONTROL = ",tombak.read_status_instruction(tombak.INSTRUCT_GATE_CONTROL))
    print("INSTRUCT_INTERN_TRIGGER_FREQ = ",tombak.read_freq_instruction(tombak.INSTRUCT_INTERN_TRIGGER_FREQ))
    print("INSTRUCT_PULSE_OUT_WIDTH = ",tombak.read_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH))
    print("INSTRUCT_PULSE_OUT_DELAY = ",tombak.read_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY))
    

    

    
    
    
    
    


















'''
tombak.set_integer_instruction(tombak.INSTRUCT_SHAPE1_STEP_NUMBER, 101)
tombak.set_integer_instruction(tombak.INSTRUCT_SHAPE1_STEP_SIZE, 2)

print("INSTRUCT_FUNCTIONING_MODE = ", tombak.read_status_instruction(tombak.INSTRUCT_FUNCTIONING_MODE)) #ok
print("INSTRUCT_PULSE_IN_THRESHOLD = ", tombak.read_float_instruction(tombak.INSTRUCT_PULSE_IN_THRESHOLD)) #ok
print("INSTRUCT_PULSE_IN_DELAY = ", tombak.read_time_instruction(tombak.INSTRUCT_PULSE_IN_DELAY)) #ok
print("INSTRUCT_PULSE_IN_SRC = ", tombak.read_status_instruction(tombak.INSTRUCT_PULSE_IN_SRC)) #ok 
print("INSTRUCT_PULSE_IN_FREQUENCY_DIV = ", tombak.read_integer_instruction(tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV))#ok
print("INSTRUCT_PULSE_OUT_DELAY = ", tombak.read_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY))#ok
print("INSTRUCT_PULSE_PULSE_OUT_WIDTH = ", tombak.read_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH))#ok
print("INSTRUCT_PULSE_BURST_SIZE = ", tombak.read_integer_instruction(tombak.INSTRUCT_PULSE_BURST_SIZE)) #ok
print("INSTRUCT_TRIGGER_SRC = ", tombak.read_status_instruction(tombak.INSTRUCT_TRIGGER_SRC)) #ok
print("INSTRUCT_INTERN_TRIGGER_FREQ = ", tombak.read_freq_instruction(tombak.INSTRUCT_INTERN_TRIGGER_FREQ))#ok
print("INSTRUCT_SYNC_OUT_1_SRC = ", tombak.read_status_instruction(tombak.INSTRUCT_SYNC_OUT_1_SRC))#ok
print("INSTRUCT_GATE_CONTROL = ", tombak.read_status_instruction(tombak.INSTRUCT_GATE_CONTROL))#ok
print("INSTRUCT_SYNC_OUT_2_SOURCE = ", tombak.read_status_instruction(tombak.INSTRUCT_SYNC_OUT_2_SOURCE))#ok
print("INSTRUCT_PULSE_OUT_INVERSION = ", tombak.read_status_instruction(tombak.INSTRUCT_PULSE_OUT_INVERSION))#ok
print("INSTRUCT_SHAPE1_STEP_NUMBER = ", tombak.read_integer_instruction(tombak.INSTRUCT_SHAPE1_STEP_NUMBER))
print("INSTRUCT_SHAPE1_STEP_SIZE = ", tombak.read_integer_instruction(tombak.INSTRUCT_SHAPE1_STEP_SIZE))
print("INSTRUCT_SHAPE2_STEP_NUMBER = ", tombak.read_integer_instruction(tombak.INSTRUCT_SHAPE2_STEP_NUMBER))
print("INSTRUCT_SHAPE2_STEP_NUMBER = ", tombak.read_integer_instruction(tombak.INSTRUCT_SHAPE2_STEP_NUMBER))
print("INSTRUCT_SHAPE3_STEP_NUMBER = ", tombak.read_integer_instruction(tombak.INSTRUCT_SHAPE3_STEP_NUMBER))
print("INSTRUCT_SHAPE3_STEP_SIZE = ", tombak.read_integer_instruction(tombak.INSTRUCT_SHAPE3_STEP_SIZE))
print("INSTRUCT_SHAPE4_STEP_NUMBER = ", tombak.read_integer_instruction(tombak.INSTRUCT_SHAPE4_STEP_NUMBER))
print("INSTRUCT_SHAPE4_STEP_NUMBER = ", tombak.read_integer_instruction(tombak.INSTRUCT_SHAPE4_STEP_SIZE))
print("INSTRUCT_PAUSE_VALUE = ", tombak.read_time_instruction(tombak.INSTRUCT_PAUSE_VALUE)) #ok
print("\n")

print("SHAPE_Configuration")
csv_table = tombak.read_csv(BATMAN)
tombak.set_integer_instruction(tombak.INSTRUCT_SHAPE1_STEP_NUMBER, csv_table[0])
tombak.set_integer_instruction(tombak.INSTRUCT_SHAPE1_STEP_SIZE)
print("INSTRUCT_SHAPE1_STEP_NUMBER = ", tombak.read_integer_instruction(tombak.INSTRUCT_SHAPE1_STEP_NUMBER))
print("INSTRUCT_SHAPE1_STEP_SIZE = ", tombak.read_integer_instruction(tombak.INSTRUCT_SHAPE1_STEP_SIZE))
tombak.send_csv(0x00, csv_table)
tombak.save_shape_data()

print("\n")
'''









