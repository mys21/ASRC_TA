/*! \file CamCmosOctUsb3.h
	\brief This file contains all CamCmosOctUsb3 data structures as well as function prototypes exported by the DLL
	\author		YDE (e2v)
	\version	1.5.1
	\date		December 2019
	\note		Supported Operating System : Windows Vista 32bits & 64 bits, Windows Seven 32bits & 64 bits, Windows 8 32bits & 64 bits, , Windows 10 32bits & 64 bits
*/
#ifndef _CAMCMOSOCTUSB3_H
#define _CAMCMOSOCTUSB3_H

#ifdef CAMCMOSOCTUSB3_EXPORTS
#define CAMCMOSOCTUSB3_API __declspec(dllexport)
#else
#define CAMCMOSOCTUSB3_API __declspec(dllimport)
#endif

#ifdef __cplusplus
	extern "C"{
#endif

/*! \defgroup CAMERA_ERROR Camera Errors
\note  Each api returns a 32 bit error code:
\note  if bit31 is set to 1 for the error code, this errors corresponds to an error defined below in the "Application Errors" section
\note  if bit31 is set to 0 for the error code, this errors corresponds to a driver error code. These errors are not defined here but you can translate it to
\note  the corresponding windows error (NtStatus or UsbdStatus) by calling api USB3_ConvertDriverErrToWindowsErr. Then you can refer to Windows documentation.
@{
*/

/*! \defgroup APPLICATION_ERROR Application Errors
@{
*/
/*! CAM_ERR_SUCCESS */
#define CAM_ERR_SUCCESS										0
/*! CAM_ERR_ERROR */
#define CAM_ERR_ERROR										-1001
/*! CAM_ERR_NOT_INITIALIZED */
#define CAM_ERR_NOT_INITIALIZED								-1002
/*! CAM_ERR_NOT_IMPLEMENTED */
#define CAM_ERR_NOT_IMPLEMENTED								-1003
/*! CAM_ERR_RESOURCE_IN_USE */
#define CAM_ERR_RESOURCE_IN_USE								-1004
/*! CAM_ERR_ACCESS_DENIED */
#define CAM_ERR_ACCESS_DENIED								-1005
/*! CAM_ERR_INVALID_HANDLE */
#define CAM_ERR_INVALID_HANDLE								-1006
/*! CAM_ERR_INVALID_ID */
#define CAM_ERR_INVALID_ID									-1007
/*! CAM_ERR_NO_DATA */
#define CAM_ERR_NO_DATA										-1008
/*! CAM_ERR_INVALID_PARAMETER */
#define CAM_ERR_INVALID_PARAMETER							-1009
/*! CAM_ERR_IO */
#define CAM_ERR_IO											-1010
/*! CAM_ERR_TIMEOUT */
#define CAM_ERR_TIMEOUT										-1011
/*! CAM_ERR_ABORT */
#define CAM_ERR_ABORT										-1012
/*! CAM_ERR_INVALID_BUFFER */
#define CAM_ERR_INVALID_BUFFER								-1013
/*! CAM_ERR_NOT_AVAILABLE */
#define CAM_ERR_NOT_AVAILABLE								-1014
/*! CAM_ERR_INVALID_ADDRESS */
#define CAM_ERR_INVALID_ADDRESS								-1015

/*! CAM_ERR_DEVICE_ALREADY_OPENED_BY_SAME_PROCESS */
#define CAM_ERR_DEVICE_ALREADY_OPENED_BY_SAME_PROCESS		-10001
/*! CAM_ERR_DEVICE_ALREADY_OPENED_BY_ANOTHER_PROCESS */
#define CAM_ERR_DEVICE_ALREADY_OPENED_BY_ANOTHER_PROCESS	-10002
/*! CAM_ERR_CAMERA_NOT_FOUND */
#define CAM_ERR_CAMERA_NOT_FOUND							-10003
/*! CAM_ERR_WRITE_REGISTER_EP0 */
#define CAM_ERR_WRITE_REGISTER_EP0							-10004
/*! CAM_ERR_READ_REGISTER_EP0 */
#define CAM_ERR_READ_REGISTER_EP0							-10005
/*! CAM_ERR_STATUS_REQUEST */
#define CAM_ERR_STATUS_REQUEST								-10006
/*! CAM_ERR_GET_IMAGE */
#define CAM_ERR_GET_IMAGE									-10007
/*! CAM_ERR_INVALID_PACKET_NB */
#define CAM_ERR_INVALID_PACKET_NB							-10008
/*! CAM_ERR_DEVICE_UNPLUGGED */
#define CAM_ERR_DEVICE_UNPLUGGED							-10009
/*! CAM_ERR_UNCOMPATIBLE_UPGRADE_PACKAGE */
#define CAM_ERR_UNCOMPATIBLE_UPGRADE_PACKAGE				-10010
/*! CAM_ERR_NOT_USB3_SUPERSPEED_PORT */
#define CAM_ERR_NOT_USB3_SUPERSPEED_PORT					-10011
/*! CAM_ERR_PACKET_LOST */
#define CAM_ERR_PACKET_LOST									-10012
/*! CAM_WARNING_FRAME_COMMPLETED_WITH_ZEROS */
#define CAM_WARNING_FRAME_COMMPLETED_WITH_ZEROS				-10013
/*!
@}
*/

/*! \defgroup FIRMWARE_ERROR_WARNING Firmware Errors and warnings
@{
*/
/*! \defgroup FIRMWARE_ERROR Firmware Errors
@{
*/
/*! CAM_ERR_FW_STATUS_INTERNAL_ERROR */
#define CAM_ERR_FW_STATUS_INTERNAL_ERROR					-20001		
/*! CAM_ERR_FW_STATUS_BAD_PARAM */
#define CAM_ERR_FW_STATUS_BAD_PARAM							-20002
/*! CAM_ERR_FW_STATUS_USB_ERROR */
#define CAM_ERR_FW_STATUS_USB_ERROR							-20003			
/*! CAM_ERR_FW_STATUS_TOO_MANY_DATA */
#define CAM_ERR_FW_STATUS_TOO_MANY_DATA						-20004
/*! CAM_ERR_FW_STATUS_OUT_OF_RANGE */
#define CAM_ERR_FW_STATUS_OUT_OF_RANGE						-20005
/*! CAM_ERR_FW_STATUS_UNKNOWN_REQUEST */
#define CAM_ERR_FW_STATUS_UNKNOWN_REQUEST					-20006
/*! CAM_ERR_FW_STATUS_ACCESS_DENIED */
#define CAM_ERR_FW_STATUS_ACCESS_DENIED						-20007
/*! CAM_ERR_FW_STATUS_BAD_ALIGNEMENT */
#define CAM_ERR_FW_STATUS_BAD_ALIGNEMENT					-20008
/*! CAM_ERR_FW_STATUS_SPI_ERROR */
#define CAM_ERR_FW_STATUS_SPI_ERROR							-20009
/*! CAM_ERR_FW_STATUS_DMA_ERROR */
#define CAM_ERR_FW_STATUS_DMA_ERROR							-20010
/*! CAM_ERR_FW_STATUS_TIMEOUT */
#define CAM_ERR_FW_STATUS_TIMEOUT							-20011
/*! CAM_ERR_FW_STATUS_BAD_USB_REQUEST */
#define CAM_ERR_FW_STATUS_BAD_USB_REQUEST					-20012
/*! CAM_ERR_FW_STATUS_FLASH_ERROR */
#define CAM_ERR_FW_STATUS_FLASH_ERROR						-20013
/*! CAM_ERR_FW_STATUS_AFE_ERROR */
#define CAM_ERR_FW_STATUS_AFE_ERROR							-20014
/*! CAM_ERR_FW_STATUS_DAC_ERROR */
#define CAM_ERR_FW_STATUS_DAC_ERROR							-20015
/*! CAM_ERR_FW_STATUS_FPGA_REG_ERROR */
#define CAM_ERR_FW_STATUS_FPGA_REG_ERROR					-20016
/*! CAM_ERR_FW_STATUS_USB_NOT_CONNECTED */
#define CAM_ERR_FW_STATUS_USB_NOT_CONNECTED					-20017
/*! CAM_ERR_FW_STATUS_ACQUISITION_ERROR */
#define CAM_ERR_FW_STATUS_ACQUISITION_ERROR					-20018
/*! CAM_ERR_FW_STATUS_FPGA_NOT_STARTED */
#define CAM_ERR_FW_STATUS_FPGA_NOT_STARTED					-20019
/*! CAM_ERR_FW_STATUS_DATA_OVERFLOW */
#define CAM_ERR_FW_STATUS_DATA_OVERFLOW						-20020
/*! CAM_ERR_FW_STATUS_ACQUSITION_ONGOING */
#define CAM_ERR_FW_STATUS_ACQUSITION_ONGOING				-20021
/*! CAM_ERR_FW_STATUS_NOT_ENOUGH_MEMORY */
#define CAM_ERR_FW_STATUS_NOT_ENOUGH_MEMORY					-20022
/*!
@}
*/
/*! \defgroup FIRMWARE_WARNING Firmware Warnings
@{
*/
/*! CAM_ERR_FW_STATUS_BUSY */
#define CAM_ERR_FW_STATUS_BUSY								-20101
/*! CAM_ERR_FW_STATUS_RETRY */
#define CAM_ERR_FW_STATUS_RETRY								-20102
/*! CAM_ERR_FW_STATUS_RETRY */
#define CAM_ERR_FW_STATUS_NEW_FIRMWARE						-20103
/*!
@}
*/
/*!
@}
*/

/*! \defgroup UPGRADE_ERROR Upgrade Errors
@{
*/
/*! CAM_ERR_MORE_THAN_ONE_CAMERA_FOUND */
#define CAM_ERR_MORE_THAN_ONE_CAMERA_FOUND					-30001
/*! CAM_ERR_FAILED */
#define CAM_ERR_FAILED										-30002
/*! CAM_ERR_INVALID_MEDIA_TYPE */
#define CAM_ERR_INVALID_MEDIA_TYPE							-30003
/*! CAM_ERR_INVALID_FWSIGNATURE */
#define CAM_ERR_INVALID_FWSIGNATURE							-30004
/*! CAM_ERR_DEVICE_CREATE_FAILED */
#define CAM_ERR_DEVICE_CREATE_FAILED						-30005
/*! CAM_ERR_INCORRECT_IMAGE_LENGTH */
#define CAM_ERR_INCORRECT_IMAGE_LENGTH						-30006
/*! CAM_ERR_INVALID_FILE */
#define CAM_ERR_INVALID_FILE								-30007
/*! CAM_ERR_SPILASH_ERASE_FAILED */
#define CAM_ERR_SPILASH_ERASE_FAILED						-30008
/*! CAM_ERR_CORRUPT_FIRMWARE_IMAGE_FILE */
#define CAM_ERR_CORRUPT_FIRMWARE_IMAGE_FILE					-30009
/*! CAM_ERR_CORRUPT_FIRMWARE_IMAGE_FILE */
#define CAM_ERR_BOOTLOADER_NOT_RUNNING						-30010
/*! CAM_ERR_UPGRADE_BULK_TRANSFER */
#define CAM_ERR_UPGRADE_BULK_TRANSFER						-30011
/*!
@}
*/

/*! \defgroup SDK_ERROR Sdk Errors
@{
*/
/*! CAM_ERR_CONTEXTUAL_DATA_DISABLED */
#define CAM_ERR_CONTEXTUAL_DATA_DISABLED					-40001
/*!
@}
*/
/*!
@}
*/


/*! \defgroup CAMERA_INFO_STRUCT Camera Info structures
@{
*/

/*! CAMERA_ID_MAX_LENGTH */
#define CAMERA_ID_MAX_LENGTH	260

/*-------------------------- */
/*! Camera Info */
typedef struct
{
	/*! Camera unique Identifier */
    char pcID[CAMERA_ID_MAX_LENGTH];
} tCameraInfo;


/*! Camera Handle */
typedef void * CAM_HANDLE;

/*! Buffer Handle */
typedef void * BUFF_HANDLE;

/*! Image Pixel Type */
typedef enum
{
	/*! Unknown Pixel Type */
	eUnknown  = 0,
	/*! Pixel Type 8 bit: Mono8 (aligned on 8 bit) */
	eMono8    = 1,
	/*! Pixel Type 10 bit: Mono10 (aligned on 16 bit) */
	eMono10   = 2,
	/*! Pixel Type 11 bit: Mono11 (aligned on 16 bit) */
	eMono11   = 3,
	/*! Pixel Type 12 bit: Mono12 (aligned on 16 bit) */
	eMono12   = 4,
} tImagePixelType;

/*! Buffer Image
  \note The Buffer can contain the image including or not MetaData(1024 bytes)
  \note The Buffer total size corresponds to the iImageSize variable
  \note The image datas are always located at the beginning of the buffer pointing by the `pDatas` variable
  \note The image size depends on ContextData activation
  \note iLinePitch = iImageWidth * GetNBytesPerPixel(eImagePixelType)
  \note iImageSize = iLinePitch * iImageHeight + ContextDataSizeInBytes
*/
typedef struct
{
	/*! Buffer handle which contains new data. */
	BUFF_HANDLE	hBuffer;     
	/* Pointer to the beginning of the image datas (including contextual datas if they are enabled) */
	void * pDatas; 
	/*! Total Buffer payload size in bytes: Width * Height * 2 + contextual datas (if there are enabled)
	\note if contextual datas are enabled, each line has a 32bit structure (see tContextDataPerLine) containing: LineCounter and NbMissedTriggers
	\note: Contextual datas start at offset: pDatas + iImageSize:
	\note  ContextualDataLine0_offset = (unsigned char *)pDatas + iImageSize + 0
	\note  ContextualDataLine1_offset = (unsigned char *)pDatas + iImageSize + sizeof(tContextDataPerLine)
	\note  ContextualDataLine2_offset = (unsigned char *)pDatas + iImageSize + 2 * sizeof(tContextDataPerLine)
	\note  ....
	\note  ContextualDataLineN_offset = (unsigned char *)pDatas + iImageSize + N * sizeof(tContextDataPerLine)
	\note  Contextual datas can also be retrieved with USB3_GetLineContextualData api
	*/
	size_t iBufferSize;
	/*! Total Image payload size in bytes: Width * Height * 2 (It does not include contextual datas) */
	size_t iImageSize;
	/*! ROI Offset X */
	size_t iOffsetX;
	/*! Width of the image (not including metadata) */
	size_t iImageWidth;
	/*! Height of the image */
	size_t iImageHeight;
	/*! Pixel Type */
	tImagePixelType eImagePixelType;
	/*! Line Pitch: corresponds to the number of bytes between two consecutive lines: Width * 2 */
	size_t iLinePitch;
	/*! Horizontal flip: 0: Disabled   1: Enabled */
	unsigned short iHorizontalFlip;
	/*! Number of missed triggers for the whole image */
	unsigned long long iNbMissedTriggers;
	/*! Number of lines lost for the whole image */
	unsigned long long iNbLineLost;
	/*! Total Image Acquired since USB3_StartAcquisition */
	unsigned long long iNbImageAcquired;
	/*! For frame trigger mode only: if there are less line triggers than expected, the buffer is completed with 0, delivered to user with the error CAM_WARNING_FRAME_COMMPLETED_WITH_ZEROS,
	   iFrameTriggerNbValidLines allows to know the valid number of lines before completion with 0.
	   For none frame triggers mode: iFrameTriggerNbValidLines is useless and is always set to 0 */
	unsigned long long iFrameTriggerNbValidLines;
	/*! If customer application is not fast enough to either call USB3_GetBuffer or USB3_RequeueBuffer, it can occur that the acquisition engines consumes all 'iNbOfBuffer' set with USB3_SetImageParameters.
	   In that case, as there are no more buffers to store camera data, it will result in data lost, and the 'iNbLineLost' will be incremented
	   'iCounterBufferStarvation' is an indicator that you can monitor to avoid the buffer starvation, it should always remain to zero */
	unsigned long long iCounterBufferStarvation;
} tImageInfos;


/*! Context datas per line
  \note If Contextual Datas are enabled, additional datas are added at the end of the image buffer: 
  \note see field pDatas of tImageInfos structure
*/
typedef struct
{
	/*! Line counter */
	unsigned short u16LineCounter;

	/*! Number of missed triggers */
	unsigned short u16NbMissedTriggers;
} tContextDataPerLine;


/*! Buffer Image */
typedef enum
{
	/*! Flush all buffers from the "Input Queue" and the "Output Queue" to the "buffer pool" */
	eFlushAllToBufferPool = 0,     
	 /*! Flush all buffers from the "buffer pool" and the "Output Queue" to the "Input Queue" */
	eFlushAllToInputQueue = 1
} tFlush;

/*! Camera plug / unplug info */
typedef enum
{
	/*! A camera was plugged */
	ePlugged = 0,     
	/*!  A camera was unplugged */
	eUnPlugged = 1
} tPlugInfo;

/*! Camera plug / unplug tPlugNotify */
typedef struct
{
	/*!  Plug info */
	tPlugInfo ePlugInfo;
	/*!  Camera ID */
	char pcCameraId[CAMERA_ID_MAX_LENGTH];
} tPlugNotify;

/*! Driver Error Type*/
typedef enum
{
	/*!  Driver Invalid Error */
	eDriverInvalidError = 0,
	/*!  Driver NtStatus error */
	eDriverNtStatus = 1,
	/*!  Driver UsbdStatus error */
	eDriverUsbdStatus = 2
} tDriverErrorType;

/*!
@}
*/


/*! \defgroup CAMERA_API Camera API
@{
*/
/*! This function allows to initialize the Camera Library			
  \return 0 if no error occurs else refers to error code list
  \note This function must be called prior to any other function call to allow global initialization of the library
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_InitializeLibrary(void);

/*! This function allows to terminate the Camera Library			
  \return 0 if no error occurs else refers to error code list
  \note This function must be called after no function of the GenTL library is needed anymore to clean up the resources from the GCInitLib function call
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_TerminateLibrary(void);

/*! This function allows to update the camera list and to get the number of cameras present on the system
  \param pulNbCameras  [out] Number of cameras found
  \n				
  \return 0 if no error occurs else refers to error code list
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_UpdateCameraList(unsigned long * pulNbCameras);

/*! This function retrieves the camera info for the given index
  \param ulIndex	    [in]  Index: range [0 to (GetCameraCount - 1)] 
  \param pCameraInfo	[out] Camera info structure
  \return 0 if no error occurs else refers to error code list
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_GetCameraInfo(unsigned long ulIndex, tCameraInfo * pCameraInfo);

/*! This function opens the communication to a camera
  \param pCameraInfo [in] The camera info (returns by USB3_UpdateCameraList)
  \param hCamera [out]  The camera handle
  \return 0 if no error occurs else refers to error code list
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_OpenCamera(const tCameraInfo * pCameraInfo, CAM_HANDLE * hCamera);

/*! This function closes the communication with the camera
  \param hCamera [in] The camera handle handle
  \return 0 if no error occurs else refers to error code list
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_CloseCamera(CAM_HANDLE hCamera);


/*! This function allows to read a camera register at a specified address
  \param hCamera   [in]     The camera handle handle  (returned by USB3_OpenCamera)
  \param ulAddress [in]     The register address to read
  \param pBuffer   [out]    Pointer to a user allocated byte buffer to receive data; this must not be NULL
  \param piSize    [in/out] Size of the provided pBuffer and thus the amount of bytes to read from the register
  \n                        after the read operation this parameter holds the information about the bytes actually read
  \return 0 if no error occurs else refers to error code list
  \note  The buffer endianess is Litte endian
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_ReadRegister(CAM_HANDLE hCamera, unsigned long ulAddress, void * pBuffer, size_t * piSize);


/*! This function allows to write a camera register at a specified address
  \param hCamera   [in]     The camera handle handle  (returned by USB3_OpenCamera)
  \param ulAddress [in]     The register address to write
  \param pBuffer   [in]     Pointer to a user allocated byte buffer to send data; this must not be NULL
  \param piSize    [in/out] Size of the provided pBuffer and thus the amount of bytes to write to the register.
  \n                        after the write operation this parameter holds the information about the bytes actually written
  \return 0 if no error occurs else refers to error code list
  \note  The buffer endianess is Litte endian
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_WriteRegister(CAM_HANDLE hCamera, unsigned long ulAddress, const void * pBuffer, size_t * piSize);

/*! This function allows to set the image parameters: height of the image and the number of buffers for the images
  \param hCamera        [in]  The camera handle handle  (returned by USB3_OpenCamera)
  \param iImageHeight   [in]  The image height (minimum value=1)
  \param iNbOfBuffer    [in] The the number of buffer to be used by acquisition engine to store received images
  \return 0 if no error occurs else refers to error code list
  \note This function can only be valled acquisition is stopped (refer to USB3_StopAcquisition)
        All buffers obtained by USB3_GetBuffer must be requeued before calling this api.
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_SetImageParameters(CAM_HANDLE hCamera, size_t iImageHeight, size_t iNbOfBuffer);

/*! This function allows to get a grabbed buffer from the SDK acquisition engine output queue 
  \param hCamera        [in]  The camera handle handle  (returned by USB3_OpenCamera)
  \param pImageInfos    [out] The tImageInfos structure allows you to get the image raw data and the image parameters
  \param ulTimeoutInMs [in]  The maximum time to wait in milliseconds. 
  \n                          if the no image can be grabbed during this time the TIMEOUT error is returned
  \n                          if you set 0xFFFFFFFF to this parameter, the timeout is infinite
  \return 0 if no error occurs else refers to error code list
  \note This api is blocking until the timeout expires, or a image is grabbed or a call to USB3_AbortGetBuffer is done.
  \n    If returned error is successfull (CAM_ERR_SUCCESS), once you don't need anymore the image datas, you must call the USB3_RequeueBuffer in order the acquisition engine can use this buffer again
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_GetBuffer(CAM_HANDLE hCamera, tImageInfos * pImageInfos, unsigned long ulTimeoutInMs);


/*! This function allows to retrieve the contextual datas of a line from a buffer
  \param hCamera        [in]  The camera handle handle  (returned by USB3_OpenCamera)
  \param pImageInfos   [in]  The tImageInfos structure returns by USB3_GetBuffer api
  \param pContextDataPerLine    [out] The tContextDataPerLine structure allows you to get the contextual datas
  \param ulLineNumber [in]  The line number:   0 <= ulLineNumber < ImageHeight. 
  \n    If returned error is successfull (CAM_ERR_SUCCESS), once you don't need anymore the image datas, you must call the USB3_RequeueBuffer in order the acquisition engine can use this buffer again
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_GetLineContextualData(CAM_HANDLE hCamera, const tImageInfos * pImageInfos, tContextDataPerLine * pContextDataPerLine, unsigned long ulLineNumber);

/*! This function allows to requeue a buffer that was successfully obtained via USB3_GetBuffer api to the input queue.
  \n After being requeued, the buffer can be used again by the SDK acquistion engine.
  \n if you don't requeue buffer, the acquisition engine risks to have a buffer starvation
  \param hCamera   [in]  The camera handle handle  (returned by USB3_OpenCamera)
  \param hBuffer   [in]  The buffer handle which was returned by USB3_GetBuffer api
  \return 0 if no error occurs else refers to error code list
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_RequeueBuffer(CAM_HANDLE hCamera, BUFF_HANDLE hBuffer);

/*! This function allows to flush all buffers from the output queue to the input queue
  \n if you don't requeue buffer, the acquisition engine risks to have a buffer starvation
  \param hCamera   [in]  The camera handle handle  (returned by USB3_OpenCamera)
  \return 0 if no error occurs else refers to error code list
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_FlushBuffers(CAM_HANDLE hCamera);

/*! This function allows to unblock any waiting call to the USB3_GetBuffer
  \param hCamera        [in]  The camera handle handle  (returned by USB3_OpenCamera)
  \return 0 if no error occurs else refers to error code list
  \note if the user was blocked on USB3_GetBuffer api, USB3_AbortGetBuffer unblocks it immediately and USB3_GetBuffer returned the ABORT_ERROR
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_AbortGetBuffer(CAM_HANDLE hCamera);

/*! This function allows to start the acquisition engine for the specified camera
  \param hCamera        [in]  The camera handle handle  (returned by USB3_OpenCamera)
  \return 0 if no error occurs else refers to error code list
  \note Once started, the acquisition engine uses all buffers in the "InputQueue" and when grabbed, move them in the "OutputQueue"
  \n where you can get back them with USB3_GetBuffer api.
  \note Before starting acquisition the SDK automatically called internally USB3_FlushQueue to reput all buffers from output to input queue
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_StartAcquisition(CAM_HANDLE hCamera);

/*! This function allows to stop the acquisition engine for the specified camera
  \param hCamera        [in]  The camera handle handle  (returned by USB3_OpenCamera)
  \note SDK automatically allocates the size of the memory for each buffer specified by USB3_SetImageParameters
  \return 0 if no error occurs else refers to error code list
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_StopAcquisition(CAM_HANDLE hCamera);

/*! This function allows to be notified of camera plug or unplug
  \param pPlugNotify   [out]  The camera notification
  \param ulTimeoutInMs [in]   The maximum time to wait in milliseconds. 
  \n                          if no camera is plugged or unnplugged during this time the TIMEOUT error is returned
  \n                          if you set 0xFFFFFFFF to this parameter, the timeout is infinite
  \return 0 if no error occurs else refers to error code list
  \note this is a blocking api
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_GetUsbNotification(tPlugNotify * pPlugNotify, unsigned long ulTimeoutInMs);

/*! This function allows to get the text corresponding to an error
  \param nErrorCode [in]  The error
  \param pcErrText  [out] A user allocated buffer to receive the texte error 
  \param piSize     [in/out] In:  The size of the pcErrText buffer
  \n                         Out: The SDK will set the exact text error size
  \return 0 if no error occurs else refers to error code list
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_GetErrorText(int nErrorCode, char * pcErrText, size_t * piSize);

/*! This function allows to tranlate a driver error to the NTStatus or UsbStatus windows error code
  \n If a CameraUSB3 api returns an error with bit31 set to zero, this error corresponds to a driver error code.
  \n In this case, this USB3_ConvertDriverErrToWindowsErr allows to translate this error to the windows corresponding error (NtStatus or UsbdStatus) 
  \param nErrorCode          [in]  The error
  \param pnWindowsErrorCode  [out] The corresponding windows error code 
  \param peDriverErrorType   [out] The driver error type 
  \return 0 if no error occurs else refers to error code list
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_ConvertDriverErrToWindowsErr(int nErrorCode, int * pnWindowsErrorCode, tDriverErrorType * peDriverErrorType);

/*! This function allows to upgrade the camera
  \param pcFw_UpgradeFileFullPath [in]  The Upgrade file full path
  \param pcPrivate [in] Reserved for manufacturer. This parameter must set to NULL
  \return 0 if no error occurs else refers to error code list
  \note Only one camera must be plugged on the system before calling this api
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_UpgradeCamera(const char * pcFw_UpgradeFileFullPath, const char * pcPrivate);

/*! This function allows to get the dlls version
  \param pcVersion  [out] A string containing the .cti version and the .dll version  
  \param piSize     [in/out] In:  The size of the pcVersion buffer
  \n                         Out: The SDK will set the exact text version size
  \return 0 if no error occurs else refers to error code list
*/
CAMCMOSOCTUSB3_API int __cdecl USB3_GetDllsVersion(char * pcVersion, size_t * piSize);

/*!
@}
*/


#ifdef __cplusplus
}
#endif

#endif /* _CAMCMOSOCTUSB3_H */
