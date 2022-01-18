from delay_class import esp301_delay_stage
import time as pytime

short_t0 = 200
ttime = 100
delay = esp301_delay_stage(short_t0)

if delay.initialized is False:
    print('Stage Not Initialized Correctly')
    #self.idling()

# uncomment to home
delay.home()

# check current position (added function to class)
currPos = delay.get_posmm()

# check to see if time is in range
# something wrong here
tcheck = delay.check_time(ttime)
if tcheck is False:
    print('Not a valid time point!')
else:
    print('Time is ok!')
    delay.move_to(ttime)
    currPos = delay.get_posmm()

#close stage
delay.close()
