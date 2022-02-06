
#include "stdafx.h"

#include <windows.h>
#include <conio.h>
#include <time.h>
#include "CamCmosOctUsb3.h"


// *******************************************************************
// Variables for TA spectroscopy
// *******************************************************************


// User defined variable
#define LINESPERFRAME                       1000            // Max value - 65535

// Fixed variables
#define WIDTH                               2048             // Line width (in pixels)
#define TRIGGER_MODE                        1                // external mixed line and frame trigger with programmable exposure time
#define CIRCULAR_BUFFER                     1                // 1 - ON | 0 - OFF
#define MAX_BULK_QUEUE_NUM                  128               // Strongly advised to set to 8 or 16 for fast aquisition cancellation
#define ENABLE_CONTEXTUAL_DATA              1                // 1 - ON | 0 - OFF
#define NUM_OF_BUFFER                       10               // Number of buffers
#define MAX_TIMEOUT_ACQ_IN_MS               10000            // 10 seconds
#define EXPOSURE_TIME                       1.32             // Max value = [LINE_PERIOD - 0.7] us | min value = 1.32 us
#define PULSE_WIDTH                         0.80             // Pulses above this value denotes a frame trigger, below this value denotes a line trigger | Units - us
#define LINE_PERIOD                         11.11            // Units - us | Given by Tombak?


// Prototype functions
void InitializeRegisters(unsigned long ulAddress, unsigned long ulValue);
void * CopyBuffer(unsigned short ** Matrix, tImageInfos ImageInfos);
void FrameData(tImageInfos ImageInfos);

// Global variable
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
	printf("Num of Cameras %p", (void*)ulNbCameras);
	USB3_GetCameraInfo(ulIndex, &CameraInfo);
	printf("\nCamera Info %s", CameraInfo);			//prints out the camera ID which can also be found when choosing the camera in the GUI
	USB3_OpenCamera(&CameraInfo, &hCamera);


	//Registers
	InitializeRegisters(0x1210C, TRIGGER_MODE);
	//InitializeRegisters(0x4F000018, CIRCULAR_BUFFER);
	//InitializeRegisters(0x4F000010, MAX_BULK_QUEUE_NUM);
	//InitializeRegisters(0x4F000000, ENABLE_CONTEXTUAL_DATA);
	InitializeRegisters(0x12128, LINESPERFRAME);
	InitializeRegisters(0x12108, EXPOSURE_TIME * 100);
	InitializeRegisters(0x12100, LINE_PERIOD * 100);
	InitializeRegisters(0x1211C, PULSE_WIDTH * 100);

	size_t iImageHeight = LINESPERFRAME;
	size_t iNbOfBuffer = NUM_OF_BUFFER;

	USB3_SetImageParameters(hCamera, iImageHeight, iNbOfBuffer);

	//Looping acquisition
	for (int n = 0; n < 100; n++) {

		USB3_StartAcquisition(hCamera);
		USB3_GetBuffer(hCamera, &ImageInfos, MAX_TIMEOUT_ACQ_IN_MS);

		FrameData(ImageInfos);

		CopyBuffer(Matrix, ImageInfos);
		free(Matrix);
		USB3_RequeueBuffer(hCamera, ImageInfos.hBuffer);
	}

	USB3_StopAcquisition(hCamera);
	USB3_FlushBuffers(hCamera);
	USB3_CloseCamera(hCamera);
	printf("\n\n*********CAMERA CLOSED********\n");
	USB3_TerminateLibrary();

	return 0;
}


void InitializeRegisters(unsigned long ulAddress, unsigned long ulValue) {
	size_t iSize = sizeof(ulValue);
	USB3_WriteRegister(hCamera, ulAddress, &ulValue, &iSize);
}


void * CopyBuffer(unsigned short ** Matrix, tImageInfos ImageInfos) {

	Matrix = (unsigned short**)malloc(sizeof(unsigned short*) * LINESPERFRAME);
	for (int i = 0; i < LINESPERFRAME; i++) 
		Matrix[i] = (unsigned short*)malloc(sizeof(unsigned short) * WIDTH);

	unsigned short pixelValues;
	for (int row = 0; row < LINESPERFRAME; row++) {
		for (int col = 0; col < WIDTH; col++) {
			
			//int index = row * col;
			pixelValues = static_cast<unsigned short*>(ImageInfos.pDatas)[row*(WIDTH)+col];
			Matrix[row][col] = pixelValues;
			//printf(" %hu ", Matrix[row][col]);

		}
	}
	return 0;
}


void FrameData(tImageInfos ImageInfos) {

	printf("\n\nImages Acquired: %llu", ImageInfos.iNbImageAcquired);
	printf("\nLines lost: %llu", ImageInfos.iNbLineLost);
	printf("\nMissed triggers: %llu", ImageInfos.iNbMissedTriggers);
	printf("\nValid lines from frame: %llu", ImageInfos.iFrameTriggerNbValidLines);
	if (ImageInfos.iCounterBufferStarvation != 0)
		printf("\nBuffer Starvation!!!!!");

}
