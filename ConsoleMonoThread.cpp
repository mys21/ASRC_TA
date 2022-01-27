
#include "stdafx.h"

#include <windows.h>
#include <conio.h>
#include <time.h>
#include "CamCmosOctUsb3.h"


// *******************************************************************
// Variables for TA spectroscopy
// *******************************************************************


// User defined variable
#define LINESPERFRAME                       45000            // Max value - 65535

// Fixed variables
#define WIDTH                               2048             // Line width (in pixels)
#define TRIGGER_MODE                        4                // external mixed line and frame trigger with programmable exposure time
#define CIRCULAR_BUFFER                     1                // 1 - ON | 0 - OFF
#define MAX_BULK_QUEUE_NUM                  16               // Strongly advised to set to 8 or 16 for fast aquisition cancellation
#define ENABLE_CONTEXTUAL_DATA              1                // 1 - ON | 0 - OFF
#define NUM_OF_BUFFER                       30               // Number of buffers
#define MAX_TIMEOUT_ACQ_IN_MS               120000           // 120 seconds
#define EXPOSURE_TIME                       1.32             // Max value = [LINE_PERIOD - 0.7] us | min value = 1.32 us
#define PULSE_WIDTH                         0.80             // Pulses above this value denotes a frame trigger, below this value denotes a line trigger | Units - us
#define LINE_PERIOD                         11.11            // Units - us | Given by Tombak?


// Prototype functions
void InitializeRegisters(unsigned long ulAddress, unsigned long ulValue);


// Global variable
CAM_HANDLE hCamera = NULL;

int main(int argc, char * argv[])
{

	unsigned long ulNbCameras;
	unsigned long ulIndex = 0;
	tCameraInfo CameraInfo;
	tImageInfos ImageInfos;

	//unsigned short ** Matrix = 0;

	// Begin
	USB3_InitializeLibrary();
	USB3_UpdateCameraList(&ulNbCameras);
	USB3_GetCameraInfo(ulIndex, &CameraInfo);
	USB3_OpenCamera(&CameraInfo, &hCamera);


	//Fixed Registers
	InitializeRegisters(0x1210C, TRIGGER_MODE);
	//USB3_ReadRegister(hCamera, 0x1210C, &ulValue, &iSize);
	InitializeRegisters(0x4F000018, CIRCULAR_BUFFER);
	InitializeRegisters(0x4F000010, MAX_BULK_QUEUE_NUM);
	InitializeRegisters(0x4F000000, ENABLE_CONTEXTUAL_DATA);
	InitializeRegisters(0x12128, LINESPERFRAME);
	InitializeRegisters(0x12108, EXPOSURE_TIME * 100);


	//Variable Registers
	InitializeRegisters(0x12100, LINE_PERIOD * 100);
	InitializeRegisters(0x1211C, PULSE_WIDTH * 100);


	size_t iImageHeight = LINESPERFRAME;
	size_t iNbOfBuffer = NUM_OF_BUFFER;


	USB3_SetImageParameters(hCamera, iImageHeight, iNbOfBuffer);

	return 0;
}


void InitializeRegisters(unsigned long ulAddress, unsigned long ulValue) {
	size_t iSize = sizeof(ulValue);
	USB3_WriteRegister(hCamera, ulAddress, &ulValue, &iSize);
}
