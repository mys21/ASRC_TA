#include "stdafx.h"

#include <windows.h>
#include <conio.h>
#include <time.h>
#include "CamCmosOctUsb3.h"


// *******************************************************************
// Variables for TA spectroscopy
// *******************************************************************


// User defined variables
#define LINE_PERIOD							11.10			// Units - us
#define PULSE_WIDTH							2.00			// Pulses above this value denotes a frame trigger, below this value denotes a line trigger

// Fixed variables
#define WIDTH                               2048             // Line width (in pixels)
#define TRIGGER_MODE                        4                // external mixed line and frame trigger with programmable exposure time
#define CIRCULAR_BUFFER                     1                // 1 - ON | 0 - OFF
#define MAX_BULK_QUEUE_NUM                  16               // Strongly advised to set to 8 or 16 for fast aquisition cancellation
#define ENABLE_CONTEXTUAL_DATA              1                // 1 - ON | 0 - OFF
#define NUM_OF_BUFFER                       30               // Number of buffers
#define MAX_TIMEOUT_ACQ_IN_MS               120000           // Two minutes
#define EXPOSURE_TIME                       1.32            // Max value = [LINE_PERIOD - 0.7] us | min value = 1.32 us
#define LINESPERFRAME                       45000            // Must be an even number, max value - 65535

// Local Exception class to manage errors
class CMyException
{
public:
	CMyException(const char * pcMsg, int nError)
	{
		::strcpy_s(m_pcMsg, sizeof(m_pcMsg), pcMsg);
		m_nError = nError;
	}
	
	void ShowReason()
	{
		if (m_nError == CAM_ERR_SUCCESS)
			printf("%s\n", m_pcMsg);
		else
		{
			char pcErrText[512];
			size_t iSize =  sizeof(pcErrText);
			if (USB3_GetErrorText(m_nError, pcErrText, &iSize) != CAM_ERR_SUCCESS)
				pcErrText[0] = '\0';

			printf("%s error : %d (%s)\n", m_pcMsg, m_nError, pcErrText);
		}
	}

public:
	char m_pcMsg[512];
	int m_nError;
};



int main(int argc, char * argv[])
{
	int nError;

    
    // *******************************************************************
    // Initialize camera for data acquisition
    // *******************************************************************
    
	try
	{
        // Initializing library
		nError = USB3_InitializeLibrary();
		if (nError != CAM_ERR_SUCCESS)
			throw CMyException("USB3_InitializeLibrary", nError);
        
        // Updating camera list
		unsigned long ulNbCameras;
		nError = USB3_UpdateCameraList(&ulNbCameras);
		if (nError != CAM_ERR_SUCCESS)
            throw CMyException("USB3_GetCameraInfo", nError);
		if (ulNbCameras == 0)
			throw CMyException("No camera found", CAM_ERR_SUCCESS);

        // Individual camera info
		tCameraInfo CameraInfo;
        unsigned long ulIndex = 0;
        nError = USB3_GetCameraInfo(ulIndex, &CameraInfo);
        if (nError == CAM_ERR_SUCCESS)
            printf("\tCamera ID: %s\n", CameraInfo.pcID);
        else
        throw CMyException("USB3_GetCameraInfo", nError);
		
        
		CAM_HANDLE hCamera = NULL;
 
        
		try
		{
			// Open camera
			nError = USB3_OpenCamera(&CameraInfo, &hCamera);
			if (nError != CAM_ERR_SUCCESS)
				throw CMyException("USB3_OpenCamera", nError);


			// ******************************************************************* 
			// Set camera registers
			// *******************************************************************

            
			unsigned long ulAddress = 0x0000;
			unsigned long ulValue;
			size_t iSize = sizeof(ulValue);
            
            
            //Registers affected by fixed variables

            
			// Trigger Mode
			ulAddress = 0x1210C;
			ulValue = TRIGGER_MODE;
			nError = USB3_WriteRegister(hCamera, ulAddress, &ulValue, &iSize);
			if (nError != CAM_ERR_SUCCESS)
				throw CMyException("USB3_WriteRegister 0x1210C", nError);
            
            
            // Circular Buffer Status
            ulAddress = 0x4F000018;
            ulValue = CIRCULAR_BUFFER;
            nError = USB3_WriteRegister(hCamera, ulAddress, &ulValue, &iSize);
            if (nError != CAM_ERR_SUCCESS)
                throw CMyException("USB3_WriteRegister 0x4F000018", nError);

            
            // Max Bulk Queue Number
            ulAddress = 0x4F000010;
            ulValue = MAX_BULK_QUEUE_NUM;
            nError = USB3_WriteRegister(hCamera, ulAddress, &ulValue, &iSize);
            if (nError != CAM_ERR_SUCCESS)
                throw CMyException("USB3_WriteRegister 0x4F000010", nError);

            
            // Enable Contextual datas
            ulAddress = 0x4F000000;
            ulValue = ENABLE_CONTEXTUAL_DATA;
            nError = USB3_WriteRegister(hCamera, ulAddress, &ulValue, &iSize);
            if (nError != CAM_ERR_SUCCESS)
                throw CMyException("USB3_WriteRegister 0x4F000000", nError);


            // Trigger Frame Line Number
            ulAddress = 0x12128;
            ulValue = LINESPERFRAME;
            nError = USB3_WriteRegister(hCamera, ulAddress, &ulValue, &iSize);
            if (nError != CAM_ERR_SUCCESS)
                throw CMyException("USB3_WriteRegister 0x12128", nError);
            
            
            // Exposure Time
            ulAddress = 0x12108;
            ulValue = EXPOSURE_TIME*100;
            nError = USB3_WriteRegister(hCamera, ulAddress, &ulValue, &iSize);
            if (nError != CAM_ERR_SUCCESS)
                throw CMyException("USB3_WriteRegister 0x12108", nError);
            
            
            // Registers affected by user defined variables
            
            
			// Line period
            ulAddress = 0x12100;
			ulValue = LINE_PERIOD*100;
			nError = USB3_WriteRegister(hCamera, ulAddress, &ulValue, &iSize);
			if (nError != CAM_ERR_SUCCESS)
				throw CMyException("USB3_WriteRegister 0x12100", nError);


			// Pulse Width
			ulAddress = 0x1211C;
			ulValue = PULSE_WIDTH*100;
			nError = USB3_WriteRegister(hCamera, ulAddress, &ulValue, &iSize);
			if (nError != CAM_ERR_SUCCESS)
				throw CMyException("USB3_WriteRegister 0x1211C", nError);


            
            // *******************************************************************
            // Set image parameters
            // *******************************************************************
            
            
            size_t iImageHeight = LINESPERFRAME;
            size_t iNbOfBuffer = NUM_OF_BUFFER;
            nError = USB3_SetImageParameters(hCamera, iImageHeight, iNbOfBuffer);
            if (nError != CAM_ERR_SUCCESS)
                throw CMyException("USB3_SetImageParameters", nError);

            
            // *******************************************************************
            // Start acquisition
            // *******************************************************************
            
            
			nError = USB3_StartAcquisition(hCamera);
			if (nError != CAM_ERR_SUCCESS)
				throw CMyException("USB3_StartAcquisition", nError);

            
            tImageInfos ImageInfos;
            unsigned long ulNBImageAcquired = 0;

            
            tContextDataPerLine ContextDataPerLine;
            bool bFirstCounter = true;
            unsigned short u16MemoLineCounter = 0;
			

            try
            {
                while ((nError == CAM_ERR_SUCCESS) && (! _kbhit()))
                {
                    nError = USB3_GetBuffer(hCamera, &ImageInfos,  MAX_TIMEOUT_ACQ_IN_MS);
                    if (nError != CAM_ERR_SUCCESS)
                        throw CMyException("USB3_GetBuffer", nError);
            
                    
                    // *************************************************************************
                    // Obtaining image from buffer
                    // *************************************************************************

                    
                    ulNBImageAcquired ++;
                    
                    // Parameters for 2D Matrix
                    unsigned short ** Matrix;
                    Matrix = (unsigned short**)malloc(sizeof(unsigned short*) * LINESPERFRAME);
                    for (int i = 0; i < LINESPERFRAME; i++)
                        Matrix[i] = (unsigned short*)malloc(sizeof(unsigned short) * WIDTH);
                    
                    
                    // Copying buffer to 2D Matrix1
                    unsigned short pixelValues;
                    for (int row = 0; row < LINESPERFRAME; row++) {
                        for (int col = 0; col < WIDTH; col++) {

                            int index = row * col;
                            pixelValues = static_cast<unsigned short*>(ImageInfos.pDatas)[row*(WIDTH)+col];
                            Matrix[row][col] = pixelValues;
                        }
                    }
                    
                    
                    //
                    // Do something with Matrix
                    //
                    
                    
                    // Free allocated memory
                    free(Matrix);
                    
                    
                    // Checking for lost lines and triggers
                    printf("\n\nLines lost: %I64u\n", ImageInfos.iNbLineLost);
                    printf("Missed triggers: %I64u\n", ImageInfos.iNbMissedTriggers);
                    
                    
                    // You must requeue the buffer to avoid buffer starvation
                    if (nError == CAM_ERR_SUCCESS)
                    {
                        nError = USB3_RequeueBuffer(hCamera, ImageInfos.hBuffer);
                        if (nError != CAM_ERR_SUCCESS)
                            throw CMyException("USB3_RequeueBuffer", nError);
                    }
                }
            }
            catch (CMyException e) // catch own CMyException
            {
                // Print Usb3 error reason
                e.ShowReason();
            }
            
            
            // *******************************************************************
            // Stop acquisition
            // *******************************************************************
            
            
			nError = USB3_StopAcquisition(hCamera);
			if (nError != CAM_ERR_SUCCESS)
				throw CMyException("USB3_StopAcquisition", nError);

            
			nError = USB3_FlushBuffers(hCamera);
			if (nError != CAM_ERR_SUCCESS)
				throw CMyException("USB3_FlushBuffers", nError);

		}
        catch (CMyException e) // catch own CMyException
        {
            // Print Usb3 error reason
            e.ShowReason();
        }
        catch (...) // Catch all other exceptions which are not caused by CMyException
        {
            // User application exception
            printf("Unknown User application exception !!!\n");
        }

        
        // Close camera
		printf("USB3_CloseCamera\n");
		nError = USB3_CloseCamera(hCamera);
		if (nError != CAM_ERR_SUCCESS)
			throw CMyException("USB3_CloseCamera", nError);
	}
	catch (CMyException e) // catch own CMyException
	{
		// Print Usb3 error reason
		e.ShowReason();
	}
    

	// Terminate Library
	printf("USB3_TerminateLibrary\n");
	nError = USB3_TerminateLibrary();
	if (nError != CAM_ERR_SUCCESS)
		printf("USB3_TerminateLibrary Error %d\n", nError);

	return 0;
}

