#main ccs

from ccs import Ccs_std

ccs_std = Ccs_std('COM7')

print("READ CONFIGURATION------------------------------------------------------")

print("INSTRUCT_SYNC_SOURCE = ",  ccs_std.read_status_instruction(ccs_std.INSTRUCT_SYNC_SOURCE))
print("INSTRUCT_PULSE_SOURCE = ",  ccs_std.read_status_instruction(ccs_std.INSTRUCT_PULSE_SOURCE))
print("INSTRUCT_FREQUENCY = ",  ccs_std.read_freq_instruction(ccs_std.INSTRUCT_FREQUENCY))
print("INSTRUCT_PULSE_WIDTH = ",  ccs_std.read_integer_instruction(ccs_std.INSTRUCT_PULSE_WIDTH))
print("INSTRUCT_DELAY = ",  ccs_std.read_time_instruction(ccs_std.INSTRUCT_DELAY))
print("INSTRUCT_OFFSET_CURRENT = ",  ccs_std.read_current_instruction(ccs_std.INSTRUCT_OFFSET_CURRENT))
print("\n")


print("SET CONFIGURATION-------------------------------------------------------")
ccs_std.set_status_instruction(ccs_std.INSTRUCT_SYNC_SOURCE,ccs_std.INTERNAL)
ccs_std.set_status_instruction(ccs_std.INSTRUCT_PULSE_SOURCE, ccs_std.INTERNAL_PULSE)
ccs_std.set_freq_instruction(ccs_std.INSTRUCT_FREQUENCY, 200000)
ccs_std.set_integer_instruction(ccs_std.INSTRUCT_PULSE_WIDTH, 123)
ccs_std.set_time_instruction(ccs_std.INSTRUCT_DELAY, 10)
ccs_std.set_current_instruction(ccs_std.INSTRUCT_OFFSET_CURRENT, 12.3)
print("\n")

print("READ CONFIGURATION------------------------------------------------------")
print("INSTRUCT_SYNC_SOURCE = ",  ccs_std.read_status_instruction(ccs_std.INSTRUCT_SYNC_SOURCE))
print("INSTRUCT_PULSE_SOURCE = ",  ccs_std.read_status_instruction(ccs_std.INSTRUCT_PULSE_SOURCE))
print("INSTRUCT_FREQUENCY = ",  ccs_std.read_status_instruction(ccs_std.INSTRUCT_FREQUENCY))
print("INSTRUCT_PULSE_WIDTH = ",  ccs_std.read_status_instruction(ccs_std.INSTRUCT_PULSE_WIDTH))
print("INSTRUCT_DELAY = ",  ccs_std.read_status_instruction(ccs_std.INSTRUCT_DELAY))
print("INSTRUCT_OFFSET_CURRENT = ",  ccs_std.read_current_instruction(ccs_std.INSTRUCT_OFFSET_CURRENT))
print("\n")



print("CURRENT PERCENT = ", ccs_std.read_percent_instruction(ccs_std.INSTRUCT_CURRENT_PERCENT))
print("TEMPERATURE = ", ccs_std.read_temperature_instruction(ccs_std.INSTRUCT_TEMPERATURE))
print("CURRENT_ALARM = ", ccs_std.read_current_instruction(ccs_std.INSTRUCT_CURRENT_ALARM))
print("CURRENT_SOURCE =", ccs_std.read_status_instruction(ccs_std.INSTRUCT_CURRENT_SOURCE))
print("INSTRUCT_READ_INTERLOCK_STATUS = ", ccs_std.read_status_instruction(ccs_std.INSTRUCT_READ_INTERLOCK_STATUS))
print("INSTRUCT_LASER_ACTIVATION = ", ccs_std.read_status_instruction(ccs_std.INSTRUCT_LASER_ACTIVATION))
