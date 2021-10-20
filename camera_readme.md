# CMOS Camera
 Camera initialization and data acquisition

The header file, CamCmosOctUsb3.h, contains the camera data structures and function prototypes exported by the DLL. Specifically, the header file defines error codes, camera initialization parameters, image parameters, buffer functions, etc. The structures and functions in the header file are used in ConsoleMonoThread.cpp to acquire data from the camera buffers and store into a memory-allocated, two dimensional array. The following information will go through the main file.


*************** General Camera Information ***************

- Teledyne e2v OCTOPLUS Modular CMOS monochrome linescan sensor of 2048 pixels
- 10x200 um pixel size
- 140ke- pixel full well capacity
- Bit depth: 12 bits
- usb3 interface


*************** VARIABLES FOR TA Spectroscopy ***************


Variables for data acquisition in TA spectroscopy are located near the beginning of ConsoleMonoThread.cpp. The variables are separated into two categories: user defined variables and fixed variables. The user defined variables for the TA experiments are:
    
- LINES_PER_FRAME
        // each integration taken by the camera becomes a line
        // defines how many lines are in single frame

- LINE_PERIOD
        // the time period between subsequent falling edges of the trigger pulses; units are in us
        // the maximum value allowed is 655.35 us
        
- EXPOSURE_TIME
        // the integration time of the camera; units are us
        // the maximum value allowed is 655.35 us
        
- PULSE_WIDTH
        // pulse durations above this value are defined as a frame triggers
        // pulse durations below this value are defined as a line triggers
        // units are in us

The user defined variables will be useful to implement into a GUI for all users of the camera. The fixed variables for the TA experiments are:

- WIDTH
        // width of the camera in pixels
        // do not change
        
- TRIGGER_MODE
        // set to: mixed external line and frame trigger with programmable exposure time mode
        // current mode allows the camera to take in two triggers
        // line trigger opens the shutter
        // frame trigger tells the camera when to start a new image and how many line triggers to accept
        
- CIRCULAR_BUFFER
        // buffers are defaulted to FIFO
        // allows the buffers to circulate in the input queue
        // prioritizes the most recent data to make sure no data is lost
        
- MAX_BULK_QUEUE_NUM
        // strongly advised to set to 8 or 16 for fast acquisition cancellation
        
- ENABLE_CONTEXTUAL_DATA
        // when enabled, allows number of missed triggers/lines to be stored in buffer
        
- NUM_OF_BUFFER
        // number of buffers
        

*************** Class: CMyExcpetion***************

This class allows exceptions to be thrown in the case that the camera retreives an error when it is initialized, register values are set, and images are acquired. For referrence, error codes may be found in CamCmosOctUsb3.h.
