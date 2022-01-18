import os
import numpy as np
from ta_data_processing_class import ta_data_processing
from TA2_camera import octoplus


if __name__ == "__main__":
	oc = octoplus()
	oc.Initialize(1000)	#45000 lines runs slow, 1000 is better for quick testing
	print('Number of Cameras: ', oc.ulNbCameras.value)
	print("Camera ID: ", oc.CameraInfo.pcID)

	oc.Acquire()
	#print("Buffer Size: ", oc.ImageInfos.iBufferSize)
	#print(oc.probe)
	#print("Max val: ", np.max(oc.probe))
	#print("Min val: ", np.min(oc.probe))
	#print("Average val: ", np.average(oc.probe))

	ta = ta_data_processing(oc.probe, oc.reference, oc.first_pixel, oc.num_pixels)
	ta.separate_on_off()
	ta.average_shots()
	#print("Pump on: ", ta.probe_on)
	#print("Pump off: ", ta.probe_off)
	oc.Exit()
