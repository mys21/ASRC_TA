09202024

Modified Burst -> 10 Hz

Divide the pump tombak by 9000 to get 10 Hz
Keep the probe running at 90 kHz, this keeps the camera buffer data acquisition fast (10 Hz, 90000 shots, ~ 0.23sec)

TA2_camera_modified_burst.py
	- line 80, self.tombakDivide, change to desired division from pump controlled tombak

Tombak_control_modified_burst.py
	- line 17, self.nDivTom, change to desired division from pump controlled tombak

ta_data_processing_class_modified_burst.py
	- line 79, tombakDivide, change to desired division from pump controlled tombak