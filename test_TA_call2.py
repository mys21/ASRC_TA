import os
import numpy as np
from ta_data_processing_class import ta_data_processing
from TA2_camera import octoplus
import keyboard

if __name__ == "__main__":
	oc = octoplus()
	oc.Initialize(10000)	#45000 lines runs slow, 1000 is better for quick testing
	print('Number of Cameras: ', oc.ulNbCameras.value)
	print("Camera ID: ", oc.CameraInfo.pcID)
	running = True


	oc.Acquire()
	print(oc.probe[oc.ImageInfos.iFrameTriggerNbValidLines-2:,:])
	np.savetxt('test_data.txt',oc.probe[oc.ImageInfos.iFrameTriggerNbValidLines-2:,:])

	#print("Buffer Size: ", oc.ImageInfos.iBufferSize)
	#print(oc.probe)
	#print("Max val: ", np.max(oc.probe))
	#print("Min val: ", np.min(oc.probe))
	#print("Average val: ", np.average(oc.probe))

	
	#ta.separate_on_off()
	#ta.average_shots()
	#print("Pump on: ", ta.probe_on)
	#print("Pump off: ", ta.probe_off)
	oc.Exit()
