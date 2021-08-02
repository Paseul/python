import sys
import clr

assembly_path = r"C:\github\python\gui\eBus\dll"
sys.path.append(assembly_path)
clr.AddReference("PvGUIDotNet")
clr.AddReference("PvDotNet")

from PvDotNet import *
from PvGUIDotNet import *
import numpy as np
import cv2

cBufferCount = 16
lBuffers = []

lForm = PvDeviceFinderForm()

lForm.ShowDialog()
lDeviceInfo = PvDeviceInfo
lDeviceInfo = lForm.Selected

mDevice = PvDevice.CreateAndConnect(lDeviceInfo)
mStream = PvStream.CreateAndOpen(lDeviceInfo)



lPayloadSize = mDevice.PayloadSize

if mStream.QueuedBufferMaximum < cBufferCount:
    lBufferCount = mStream.QueuedBufferMaximum
else:
    lBufferCount = cBufferCount

for i in range(lBufferCount):
    lBuffers.append(PvBuffer())
    mStream.QueueBuffer(lBuffers[i])

mDevice.StreamEnable()
mDevice.Parameters.ExecuteCommand("AcquisitionStart")

while(True):
    lBuffer = None
    lOperationResult = PvResult(PvResultCode.OK)

    lResult = mStream.RetrieveBuffer(lBuffer, lOperationResult, np.int32(100))
    for i in range(len(lResult)):
        print(lResult[i])

    if (lResult[0].IsOK):
        if (lOperationResult.IsOK):
            print(lBuffer[0])
            mStream.QueueBuffer(lBuffer)
