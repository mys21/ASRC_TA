import os
import numpy as np
from enum import IntEnum	
from time import time, sleep
import datetime
from math import ceil, floor
from TA2_camera1 import UTC_IR_Camera

camera = UTC_IR_Camera()

camera.Initialize(lines_per_frame = 3000)
camera.Acquire()
camera.Exit()
