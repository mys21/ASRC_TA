
#include "stdafx.h"

#include <windows.h>
#include <conio.h>
#include <time.h>
#include "CamCmosOctUsb3.h"


// *******************************************************************
// Variables for TA spectroscopy
// *******************************************************************


// User defined variables
#define LINE_PERIOD                         11.10            // Units - us
#define PULSE_WIDTH                         0.80             // Pulses above this value denotes a frame trigger, below this value denotes a line trigger

// Fixed variables
#define WIDTH                               2048             // Line width (in pixels)
#define TRIGGER_MODE                        4                // external mixed line and frame trigger with programmable exposure time
#define CIRCULAR_BUFFER                     1                // 1 - ON | 0 - OFF
#define MAX_BULK_QUEUE_NUM                  16               // Strongly advised to set to 8 or 16 for fast aquisition cancellation
#define ENABLE_CONTEXTUAL_DATA              1                // 1 - ON | 0 - OFF
#define NUM_OF_BUFFER                       30               // Number of buffers
#define MAX_TIMEOUT_ACQ_IN_MS               120000           // 120 seconds
#define EXPOSURE_TIME                       1.32             // Max value = [LINE_PERIOD - 0.7] us | min value = 1.32 us
#define LINESPERFRAME                       50000            // Must be an even number, max value - 65535 | 45000 = 90000/2


// Prototype functions
void InitializeRegisters(unsigned long ulAddress, unsigned long ulValue);
void * CopyBuffer(unsigned short ** Matrix, tImageInfos ImageInfos);

// Global Variable
CAM_HANDLE hCamera = NULL;

int main(int argc, char * argv[])
{

	unsigned long ulNbCameras;
	unsigned long ulIndex = 0;
	tCameraInfo CameraInfo;
	tImageInfos ImageInfos;

	unsigned short ** Matrix = 0;

	// Begin
	USB3_InitializeLibrary();
	USB3_UpdateCameraList(&ulNbCameras);
	USB3_GetCameraInfo(ulIndex, &CameraInfo);
	USB3_OpenCamera(&CameraInfo, &hCamera);


	//Fixed Registers
	InitializeRegisters(0x1210C, TRIGGER_MODE);
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
	USB3_StartAcquisition(hCamera);

	USB3_GetBuffer(hCamera, &ImageInfos, MAX_TIMEOUT_ACQ_IN_MS);
	CopyBuffer(Matrix, ImageInfos);


	//Do something with 2D array / process data


	//Free allocated memory
	free(Matrix);

	// End
	USB3_RequeueBuffer(hCamera, ImageInfos.hBuffer);
	USB3_StopAcquisition(hCamera);
	USB3_FlushBuffers(hCamera);
	USB3_CloseCamera(hCamera);
	USB3_TerminateLibrary();

	return 0;
}


void InitializeRegisters(unsigned long ulAddress, unsigned long ulValue) {
	size_t iSize = sizeof(ulValue);
	USB3_WriteRegister(hCamera, ulAddress, &ulValue, &iSize);
}


void * CopyBuffer(unsigned short ** Matrix, tImageInfos ImageInfos) {

	// Memory allocation for 2D Matrix
	Matrix = (unsigned short**)malloc(sizeof(unsigned short*) * LINESPERFRAME);
	for (int i = 0; i < LINESPERFRAME; i++)
		Matrix[i] = (unsigned short*)malloc(sizeof(unsigned short) * WIDTH);

	// Copying buffer to 2D Matrix
	unsigned short pixelValues;
	for (int row = 0; row < LINESPERFRAME; row++) {
		for (int col = 0; col < WIDTH; col++) {

			int index = row * col;
			pixelValues = static_cast<unsigned short*>(ImageInfos.pDatas)[row*(WIDTH)+col];
			Matrix[row][col] = pixelValues;
		}
	}
	return 0;
}
