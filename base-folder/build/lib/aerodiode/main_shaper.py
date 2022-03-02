#Main file

from shaper import Shaper

#Define
SQUARE1 = "csv_png/square-50ns-1A-5ps-100pts.csv"  
SQUARE2 = "csv_png/square-100ns-1A-1ns-100pts.csv" 
SQUARE3 = "csv_png/square-200ns-1A-2ns-100pts.csv" 
GAUSSIAN1 = "csv_png/gaussian-100ns-1A-10ns-2-1ns-101pts.csv" 
SINUS1 = "csv_png/sinus-100ns-1A-10ns-2deg-1ns-100pts.csv" 
EXPONENTIAL1 = "csv_png/exponential-100ns-1A-10-1ns-100pts.csv" 

#Shaper CONNECTION-------------------------------------------------
shaper = Shaper('COM9')

#Laser Activation
print("Laser activation...")
shaper.set_status_instruction(shaper.INSTRUCT_LASER_ACTIVATION, shaper.VALUE_LASER_ON) #set status
shaper.apply_all()
print("LASER_ACTIVATION = ", shaper.read_status_instruction(shaper.INSTRUCT_LASER_ACTIVATION)) #read status
print("\n")

print("Alarm configuration-----------------------------------------")
print("ALARMS_ENABLE---")
shaper.alarm_enable["laser_temperature"] = 1    #modif alarm enable
shaper.set_alarm_enable()                       #apply modification
print(shaper.read_alarm_enable())

print("Read Measure------------------------------------------------")
print("MAIN VOLTAGE = ", shaper.measure_main_voltage(), " W")
shaper.read_alarm_state()
print("ALARM STATE = ", shaper.alarm_state)
print("\n")

print("CURRENT CONFIGURATION------------------------------------")
print("INSTRUCT_PEAK_CURRENT_MODULATION = ", shaper.read_current_instruction(shaper.INSTRUCT_PEAK_CURRENT_MODULATION), " A") #read current

print("TRIGGER CONFIGURATION------------------------------------")
shaper.set_status_instruction(shaper.INSTRUCT_TRIGGER_SYNCHRO_SOURCE_A, shaper.SYNC_INTERNAL) #read status
print("TRIGGER_SYNCHRO_SOURCE_A = ", shaper.read_status_instruction(shaper.INSTRUCT_TRIGGER_SYNCHRO_SOURCE_A)) #set status
print("\n")

print("Frequency Configuration----------------------------------")
FREQUENCY = 100000 #100kHz
shaper.set_freq_instruction(shaper.INSTRUCT_INTERNAL_SYNC_FREQUENCY_A, FREQUENCY);              #set frequency
print("INSTRUCT_INTERNAL_SYNC_FREQUENCY_A = ", shaper.read_freq_instruction(shaper.INSTRUCT_INTERNAL_SYNC_FREQUENCY_A), " Hz") #read frequency
print("\n")

print("Sequence A Configuartion")
shaper.sequence_a['LAST_VALID_ID'] = 1 #modif Sequence A 1
shaper.sequence_a['ID1'] = shaper.SHAPE1 #modif Sequence A 2
shaper.set_sequence_a()                 #apply modification
print(shaper.read_sequence_a())

print("SEND A CSV TO SHAPE 1------------------------------------------")
shaper.set_step_instruction(shaper.INSTRUCT_SHAPE1_STEP_COUT, 101)  #shape width = (STEP_COUT*STEP_SIZE)/2
shaper.set_step_instruction(shaper.INSTRUCT_SHAPE1_STEP_SIZE, 2)


table_csv = shaper.read_csv(SQUARE1)                                                                           
shaper.send_csv(shaper.SHAPE1, table_csv)
shaper.play_shape(shaper.SHAPE1)
shaper.apply_all()
print("\n")

print("TRIGGER OUT CONFIGURATION")
print("INSTRUCT_SHAPE1_TRIG_OUT2_DELAY = ", shaper.read_time_instruction(shaper.INSTRUCT_SHAPE1_TRIG_OUT2_DELAY))
print("INSTRUCT_SHAPE1_TRIG_OUT2_PULSE_WIDTH = ", shaper.read_time_instruction(shaper.INSTRUCT_SHAPE1_TRIG_OUT2_PULSE_WIDTH))
shaper.set_time_instruction(shaper.INSTRUCT_SHAPE1_TRIG_OUT2_DELAY, 100)                                                        #set time
shaper.set_time_instruction(shaper.INSTRUCT_SHAPE1_TRIG_OUT2_PULSE_WIDTH, 10)                                                   #read time
print("\n")







