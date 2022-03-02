#Main file

from central import Central

## Central CONNECTION-------------------------------------------------
central = Central('COM5')

print("measure_time_alarm_since_alarm_triggered = ", central.measure_time_alarm_since_alarm_triggered())
print(central.read_watchdog_pd_pulse_photo())