import sys
import clr

assembly_path = r"C:\github\python\gui\eBus\dll"
sys.path.append(assembly_path)
clr.AddReference("PvGUIDotNet")
clr.AddReference("PvDotNet")

from PvDotNet import *
from PvGUIDotNet import *

PvDeviceInfo.lForm = PvDeviceFinderForm()
PvDeviceInfo lForm

PvDeviceInfo.lForm.ShowDialog()
lDeviceInfo = PvDeviceInfo
lDeviceInfo = PvDeviceInfo.lForm.Selected
print(lDeviceInfo)
mDevice = PvDevice.CreateAndConnect(lDeviceInfo)
mStream = PvStream.CreateAndOpen(lDeviceInfo)

PvDeviceGEV.lDGEV = mDevice
PvDeviceGEV.lDGEV.NegotiatePacketSize()

PvStreamGEV.lSGEV = mStream
PvDeviceGEV.lDGEV.SetStreamDestination(PvStreamGEV.lSGEV.LocalIPAddress, PvStreamGEV.lSGEV.LocalPort)