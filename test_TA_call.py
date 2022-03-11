import os
import numpy as np
from ta_data_processing_class import ta_data_processing
from TA2_camera import octoplus
import keyboard

if __name__ == "__main__":
	oc = octoplus()
	shots = input("Number of lines: ")
	shots = int(shots)
	oc.Initialize(shots)
	print('Number of Cameras: ', oc.ulNbCameras.value)
	print("Camera ID: ", oc.CameraInfo.pcID)
	print("Start time: ", oc.current_day_time)
	#oc.Acquire()

	for i in range(5):
		oc.Acquire()
		print(i+1," :")

#	running = True
#	count = 1
#	while running == True:
#		try:
#			oc.Acquire()
#			print(count+1)
#			#print(oc.current_time)
#			count = count+1
#			if keyboard.is_pressed('q'):
#				print("\nq pressed, ending acquire loop")
#				break		
#		except OSError:
#			print("Requeue Error!")
#			running = False
#			break

	#print("Buffer Size: ", oc.ImageInfos.iBufferSize)
	#print(oc.probe)
	#print("Max val: ", np.max(oc.probe))
	#print("Min val: ", np.min(oc.probe))
	#print("Average val: ", np.average(oc.probe))

	#ta = ta_data_processing(oc.probe, oc.first_pixel, oc.num_pixels)
	#ta.separate_on_off()
	#ta.average_shots()
	#print("Pump on: ", ta.probe_on)
	#print("Pump off: ", ta.probe_off)
	oc.Exit()
