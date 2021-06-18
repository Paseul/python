#=========================================================================
# Newport Proprietary and Confidential Newport Corporation @2012
#
# No part of this file in any format, with or without modification
# shall be used, copied or distributed without the express written
# consent of Newport Corporation.
#
# Description: This is a Python Script to access CONEX-LDS library
#=========================================================================
# Initialization Start
# The script within Initialization Start and Initialization End is needed for
# properly initializing Command Interface for Conex-LDS instrument.
# The user should copy this code as is and specify correct paths here.
import sys
# Command Interface DLL can be found here.
print ("Adding location of Newport.CONEXLDS.CommandInterface.dll to sys.path")
sys.path.append(r'C:\Newport\MotionControl\CONEX-LDS\Bin')
# The CLR module provide functions for interacting with the underlying
# .NET runtime
import clr
# Add reference to assembly and import names from namespace
clr.AddReference(r'C:\Newport\Motion Control\CONEX-LDS\Bin\64-bit\Newport.CONEXLDS.CommandInterface.dll')
from CommandInterfaceConexLDS import *
import System
#=========================================================================
# Constant
ON = 1
OFF = 0
#*************************************************
# Procedure to open communication with instrument.
#*************************************************
def CONEXLDS_Open (instrumentKey):
    # Create a CONEX-LDS instance
    LDS = ConexLDS()

    print ('Instrument Key=>', instrumentKey)
    ret = LDS.OpenInstrument(instrumentKey)
    print ('OpenInstrument => ', ret)

    return LDS

#*************************************************
# Procedure to close communication.
#*************************************************
def CONEXLDS_Close(LDS):
    LDS.CloseInstrument()

#*************************************************
# Procedure to get the controller version (VE)
#*************************************************
def CONEXLDS_GetControllerVersion (LDS, address, flag):
    result, version, errString = LDS.VE(address)
    if flag == 1:
        if result == 0:
            print('CONEX-LDS firmware version => ', version)
    else:
        print('VE Error => ', errString)
    return result, version


# *************************************************
# Procedure to get the laser status (GP Command)
# *************************************************
def CONEXLDS_GetPositionsAndLightLevel(LDS, address, flag):
    # Get X, Y positions and light level Using GP Command
    result, posX, posY, lightLevel, errString = LDS.GP(address)
    if flag == 1:
        if result == 0:
            print('Position X => ', posX)
            print('Position Y => ', posY)
            print('Light level => ', lightLevel, "%")
        else:
            print('GP Error => ', errString)
    return result, posX, posY, lightLevel


# *************************************************
# Procedure to get the laser status (LB? Command)
# *************************************************
def CONEXLDS_GetLaserStatus(LDS, address, flag):
    result, laserStatus, errString = LDS.LB_Get(address)
    if flag == 1:
        if result == 0:
            print('Laser status => ', laserStatus)
    else:
        print('LB_Get Error => ', errString)
    return result, laserStatus


# *************************************************
# Procedure to set the laser status (LB Command)
# *************************************************
def CONEXLDS_SetLaserStatus(LDS, address, laserStatus, flag):
    result, errString = LDS.LB_Set(address, laserStatus)
    if flag == 1:
        if result != 0:
            print('LB_Set Error => ', errString)
    return result


# *************************************************
# Main
# *************************************************

# Initialization
instrument = "COM19"
displayFlag = 1
address = 1
# Create a CONEX-LDS interface and open communication.
LDS = CONEXLDS_Open(instrument)
# Get controller revision information
result, version = CONEXLDS_GetControllerVersion(LDS, address, displayFlag)

# Get laser status
result, iLaserStatus = CONEXLDS_GetLaserStatus(LDS, address, displayFlag)
if result == 0:
# If the laser is OFF then turn the laser ON
# Check and refresh the laser status
    if iLaserStatus == OFF:
        print('Laser is OFF')
        result = CONEXLDS_SetLaserStatus(LDS, address, ON, displayFlag)
        result, iLaserStatus = CONEXLDS_GetLaserStatus(LDS, address, displayFlag)
# Get positions
if iLaserStatus == ON:
    print('Laser is ON')
    # Get X, Y positions and light level
    returnValue, positionX, positionY, lightLevel = CONEXLDS_GetPositionsAndLightLevel(LDS, address, displayFlag)
# close communication.
CONEXLDS_Close(LDS)
print('End of script')