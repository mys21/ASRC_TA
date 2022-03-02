#Main file

from central import Central

## Central CONNECTION-------------------------------------------------
central = Central('COM5')

print("TEST ALARM")
print("alarm enable = ", central.read_alarm_enable())
print("\n")
print("alarm behavior 1 = ",central.read_alarm_behavior1())
print("\n")
print("alarm behavior 2 = ",central.read_alarm_behavior2())
print("\n")
print("read_alarm_history = ", central.read_alarm_history())
print("\n")
print("read_alarm_status = ", central.read_alarm_status())
print("\n\n")
print("SET NEW Alarm instruction")
central.alarm_enable['T_CASE'] = 0
central.alarm_behavior1['BAD_START_SEQ'] = 1
central.alarm_behavior2['BAD_START_SEQ'] = 1
central.alarm_history['BAD_START_SEQ'] = 1
central.set_alarm_enable();
central.set_alarm_behavior1()
central.set_alarm_behavior2();
central.set_alarm_history()
print("\n\n")
print("TEST NEW ALARM")
print("alarm enable = ", central.read_alarm_enable())
print("\n")
print("alarm behavior 1 = ",central.read_alarm_behavior1())
print("\n")
print("alarm behavior 2 = ",central.read_alarm_behavior2())
print("\n")
print("read_alarm_history = ", central.read_alarm_history())
print("\n")
print("read_alarm_status = ", central.read_alarm_status())
print("\n\n")
print("TEST MEASURE")
print("measure_main_v_mon = ", central.measure_main_v_mon())
print("measure_hk_v_mon = ", central.measure_hk_v_mon())
print("measure_red_guide_v_mon = ", central.measure_red_guide_v_mon())
print("measure_smd1_t = ", central.measure_smd1_t())
print("measure_smd2_t = ", central.measure_smd2_t())
print("measure_case_t = ", central.measure_case_t())
print("measure_smd1_current = ", central.measure_smd1_current())
print("measure_pd_out_power = ", central.measure_pd_out_power())
print("measure_main_v_mon = ", central.measure_pd_bra_power())
print("measure_pd_in_cw_power = ", central.measure_pd_in_cw_power())
print("measure_pd_inter_power = ", central.measure_pd_inter_power())
print("measure_pd_cri_power = ", central.measure_pd_cri_power())
#print("measure_ext_sync_freq = ", central.measure_ext_sync_freq())
print("measure_latched_interlocked_alarmn = ", central.measure_latched_interlocked_alarm())
#print("measure_time_alarm_since_alarm_triggered = ", central.measure_time_alarm_since_alarm_triggered())
print("measure_pd_out_pulse_acc_time = ", central.measure_pd_out_pulse_acc_time())
print("measure_pd_cri_pulse_acc_time = ", central.measure_pd_cri_pulse_acc_time())
print("measure_fsm_current_state = ", central.measure_fsm_current_state())
print("measure_pd_out_pulse_acc_time = ", central.measure_pd_out_pulse_acc_time())
print("measure_analog_spare_kk0 = ", central.measure_analog_spare_kk0())
print("measure_analog_spare_kk1 = ", central.measure_analog_spare_kk1())
