from ctypes import *
import os
from test_header import octoplus

if __name__ == "__main__":
    oc = octoplus()
    oc.Initialize()
    oc.Acquire()