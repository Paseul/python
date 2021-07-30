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

lForm = PvDeviceFinderForm()

lForm.ShowDialog()
lDeviceInfo = PvDeviceInfo
lDeviceInfo = lForm.Selected
print(lDeviceInfo)
mDevice = PvDevice.CreateAndConnect(lDeviceInfo)
mStream = PvStream.CreateAndOpen(lDeviceInfo)

lPayloadSize = mDevice.PayloadSize
if mStream.QueuedBufferMaximum < cBufferCount:
    lBufferCount = mStream.QueuedBufferMaximum
else:
    lBufferCount = cBufferCount


for i in range(lBufferCount):
    lBuffers[i] = PvBuffer()
    mStream.QueueBuffer(lBuffers[i])

lBuffer = None
lBuffer = PvBuffer(lBuffer)

lOperationResult = PvResult(PvResultCode.OK)
mDevice.StreamEnable()
mDevice.Parameters.ExecuteCommand("AcquisitionStart")

while(True):
    lResult = mStream.RetrieveBuffer(lBuffer, lOperationResult, np.int32(100))
    for i in range(len(lResult)):
        print(lResult[i])

    if (lResult[0].IsOK):
        if (lOperationResult.IsOK):
            print(lBuffer[0])
            mStream.QueueBuffer(lBuffer)
