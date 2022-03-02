from ccm import Ccm

ccm = Ccm('COM7')

print("CONFIGURATION----------------------------------------")
print("CURRENT SOURCE = ", ccm.read_status_instruction(ccm.INSTRUCT_CURRENT_SOURCE))
print("LASER SLOPE = ", ccm.read_time_instruction(ccm.INSTRUCT_LASER_SLOPE))
print("LASER TEMPERATURE = ", ccm.read_temperature_instruction(ccm.INSTRUCT_LASER_TEMPERATURE))
print("DC VOLTAGE = ", ccm.read_voltage_instruction(ccm.INSTRUCT_DC_VOLTAGE))
print("DC_VOLTAGE_MODE = ", ccm.read_status_instruction(ccm.INSTRUCT_DC_VOLTAGE_MODE))
print("APC MODE = ", ccm.read_status_instruction(ccm.INSTRUCT_APC_MODE))
print("DC MAX VOLTAGE = ", ccm.read_voltage_instruction(ccm.INSTRUCT_DC_MAX_VOLTAGE))
print("TEC_MODE = ", ccm.read_status_instruction(ccm.INSTRUCT_TEC_MODE))
print("FUNCTIONMENT_MODE = ", ccm.read_status_instruction(ccm.INSTRUCT_FUNCTIONMENT_MODE))
print("PULSE_FREQUENCY = ", ccm.read_status_instruction(ccm.INSTRUCT_PULSE_FREQUENCY))
print("PULSE_WIDTH = ", ccm.read_status_instruction(ccm.INSTRUCT_PULSE_WIDTH))
print("PULSE_LASER_MODE = ", ccm.read_status_instruction(ccm.INSTRUCT_PULSE_LASER_MODE))
print("PULSE_GATE_MODE = ", ccm.read_status_instruction(ccm.INSTRUCT_PULSE_GATE_MODE))
print("BURST_COUNT = ", ccm.read_integer_instruction(ccm.INSTRUCT_BURST_COUNT))






print("\n")

print("SET CONFIGURATION----------------------------------------")
ccm.set_status_instruction(ccm.INSTRUCT_CURRENT_SOURCE, ccm.EXTERNAL)
ccm.set_time_instruction(ccm.INSTRUCT_LASER_SLOPE, 2)
ccm.set_temperature_instruction(ccm.INSTRUCT_LASER_TEMPERATURE, 6)
ccm.set_voltage_instruction(ccm.INSTRUCT_DC_VOLTAGE, 5.0)
ccm.set_status_instruction(ccm.INSTRUCT_DC_VOLTAGE_MODE, ccm.AUTOMATIC)
ccm.set_status_instruction(ccm.INSTRUCT_APC_MODE, ccm.EXT_INT)
ccm.set_voltage_instruction(ccm.INSTRUCT_DC_MAX_VOLTAGE, 25)
ccm.set_status_instruction(ccm.INSTRUCT_TEC_MODE, ccm.AUTOMATIC)
ccm.set_status_instruction(ccm.INSTRUCT_FUNCTIONMENT_MODE, ccm.AUTOMATIC)
ccm.set_freq_instruction(ccm.INSTRUCT_PULSE_FREQUENCY, 255000)
ccm.set_time_instruction(ccm.INSTRUCT_PULSE_WIDTH, 10)
ccm.set_status_instruction(ccm.INSTRUCT_PULSE_GATE_MODE, ccm.SOFT)
ccm.set_integer_instruction(ccm.INSTRUCT_BURST_COUNT, 200)


print("\n")

print("CHECK CONFIGURATION---------------------------------------")
print("CURRENT SOURCE = ",  ccm.read_status_instruction(ccm.INSTRUCT_CURRENT_SOURCE))
print("LASER SLOPE = ", ccm.read_time_instruction(ccm.INSTRUCT_LASER_SLOPE))
print("LASER TEMPERATURE = ", ccm.read_temperature_instruction(ccm.INSTRUCT_LASER_TEMPERATURE))
print("DC VOLTAGE = ", ccm.read_voltage_instruction(ccm.INSTRUCT_DC_VOLTAGE))
print("DC_VOLTAGE_MODE = ", ccm.read_status_instruction(ccm.INSTRUCT_DC_VOLTAGE_MODE))
print("APC MODE = ", ccm.read_status_instruction(ccm.INSTRUCT_APC_MODE))
print("DC MAX VOLTAGE = ", ccm.read_voltage_instruction(ccm.INSTRUCT_DC_MAX_VOLTAGE))
print("TEC_MODE = ", ccm.read_status_instruction(ccm.INSTRUCT_TEC_MODE))
print("FUNCTIONMENT_MODE = ", ccm.read_status_instruction(ccm.INSTRUCT_FUNCTIONMENT_MODE))
print("PULSE_FREQUENCY = ", ccm.read_status_instruction(ccm.INSTRUCT_PULSE_FREQUENCY))
print("PULSE_WIDTH = ", ccm.read_status_instruction(ccm.INSTRUCT_PULSE_WIDTH))
print("PULSE_LASER_MODE = ", ccm.read_status_instruction(ccm.INSTRUCT_PULSE_LASER_MODE))
print("PULSE_GATE_MODE = ", ccm.read_status_instruction(ccm.INSTRUCT_PULSE_GATE_MODE))
print("BURST_COUNT = ", ccm.read_integer_instruction(ccm.INSTRUCT_BURST_COUNT))

print("Test alarme-----------------------------------------------")
print(ccm.read_alarm_status())
