from mmd import Mmd

mmd = Mmd('COM12')

print("CONFIGURATION----------------------------------------")
print("CURRENT SOURCE = ", mmd.read_status_instruction(mmd.INSTRUCT_CURRENT_SOURCE))
print("LASER SLOPE = ", mmd.read_time_instruction(mmd.INSTRUCT_LASER_SLOPE))
print("LASER TEMPERATURE = ", mmd.read_temperature_instruction(mmd.INSTRUCT_LASER_TEMPERATURE))
print("DC VOLTAGE = ", mmd.read_voltage_instruction(mmd.INSTRUCT_DC_VOLTAGE))
print("DC_VOLTAGE_MODE = ", mmd.read_status_instruction(mmd.INSTRUCT_DC_VOLTAGE_MODE))
print("APC MODE = ", mmd.read_status_instruction(mmd.INSTRUCT_APC_MODE))
print("DC MAX VOLTAGE = ", mmd.read_voltage_instruction(mmd.INSTRUCT_DC_MAX_VOLTAGE))
print("TEC_MODE = ", mmd.read_status_instruction(mmd.INSTRUCT_TEC_MODE))
print("FUNCTIONMENT_MODE = ", mmd.read_status_instruction(mmd.INSTRUCT_FUNCTIONMENT_MODE))
print("PULSE_FREQUENCY = ", mmd.read_status_instruction(mmd.INSTRUCT_PULSE_FREQUENCY))
print("PULSE_WIDTH = ", mmd.read_status_instruction(mmd.INSTRUCT_PULSE_WIDTH))
print("PULSE_LASER_MODE = ", mmd.read_status_instruction(mmd.INSTRUCT_PULSE_LASER_MODE))
print("PULSE_GATE_MODE = ", mmd.read_status_instruction(mmd.INSTRUCT_PULSE_GATE_MODE))
print("BURST_COUNT = ", mmd.read_integer_instruction(mmd.INSTRUCT_BURST_COUNT))






print("\n")

print("SET CONFIGURATION----------------------------------------")
mmd.set_status_instruction(mmd.INSTRUCT_CURRENT_SOURCE, mmd.EXTERNAL)
mmd.set_time_instruction(mmd.INSTRUCT_LASER_SLOPE, 2)
mmd.set_temperature_instruction(mmd.INSTRUCT_LASER_TEMPERATURE, 6)
mmd.set_voltage_instruction(mmd.INSTRUCT_DC_VOLTAGE, 5.0)
mmd.set_status_instruction(mmd.INSTRUCT_DC_VOLTAGE_MODE, mmd.AUTOMATIC)
mmd.set_status_instruction(mmd.INSTRUCT_APC_MODE, mmd.EXT_INT)
mmd.set_voltage_instruction(mmd.INSTRUCT_DC_MAX_VOLTAGE, 25)
mmd.set_status_instruction(mmd.INSTRUCT_TEC_MODE, mmd.AUTOMATIC)
mmd.set_status_instruction(mmd.INSTRUCT_FUNCTIONMENT_MODE, mmd.AUTOMATIC)
mmd.set_freq_instruction(mmd.INSTRUCT_PULSE_FREQUENCY, 255000)
mmd.set_time_instruction(mmd.INSTRUCT_PULSE_WIDTH, 10)
mmd.set_status_instruction(mmd.INSTRUCT_PULSE_GATE_MODE, mmd.SOFT)
mmd.set_integer_instruction(mmd.INSTRUCT_BURST_COUNT, 200)


print("\n")

print("CHECK CONFIGURATION---------------------------------------")
print("CURRENT SOURCE = ",  mmd.read_status_instruction(mmd.INSTRUCT_CURRENT_SOURCE))
print("LASER SLOPE = ", mmd.read_time_instruction(mmd.INSTRUCT_LASER_SLOPE))
print("LASER TEMPERATURE = ", mmd.read_temperature_instruction(mmd.INSTRUCT_LASER_TEMPERATURE))
print("DC VOLTAGE = ", mmd.read_voltage_instruction(mmd.INSTRUCT_DC_VOLTAGE))
print("DC_VOLTAGE_MODE = ", mmd.read_status_instruction(mmd.INSTRUCT_DC_VOLTAGE_MODE))
print("APC MODE = ", mmd.read_status_instruction(mmd.INSTRUCT_APC_MODE))
print("DC MAX VOLTAGE = ", mmd.read_voltage_instruction(mmd.INSTRUCT_DC_MAX_VOLTAGE))
print("TEC_MODE = ", mmd.read_status_instruction(mmd.INSTRUCT_TEC_MODE))
print("FUNCTIONMENT_MODE = ", mmd.read_status_instruction(mmd.INSTRUCT_FUNCTIONMENT_MODE))
print("PULSE_FREQUENCY = ", mmd.read_status_instruction(mmd.INSTRUCT_PULSE_FREQUENCY))
print("PULSE_WIDTH = ", mmd.read_status_instruction(mmd.INSTRUCT_PULSE_WIDTH))
print("PULSE_LASER_MODE = ", mmd.read_status_instruction(mmd.INSTRUCT_PULSE_LASER_MODE))
print("PULSE_GATE_MODE = ", mmd.read_status_instruction(mmd.INSTRUCT_PULSE_GATE_MODE))
print("BURST_COUNT = ", mmd.read_integer_instruction(mmd.INSTRUCT_BURST_COUNT))

print("Test alarme-----------------------------------------------")
print(mmd.read_alarm_status())
