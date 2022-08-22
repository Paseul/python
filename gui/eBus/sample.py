import clr
import sys
assembly_path = r"C:\github\python\gui\eBus\dll"
sys.path.append(assembly_path)
clr.AddReference("PvGUIDotNet")
clr.AddReference("PvDotNet")

import PvDotNet
import PvGUIDotNet
from PvDotNet import *
from PvGUIDotNet import *
import numpy as np

lForm = PvDeviceFinderForm()

lForm.ShowDialog()
lDeviceInfo = lForm.Selected

mDevice = PvDevice.CreateAndConnect(lDeviceInfo)
mStream = PvStream.CreateAndOpen(lDeviceInfo)

DeviceGEV = PvDeviceGEV()
Stream = PvStreamGEV()

LocalIP = Stream.LocalIPAddress
LocalPort = Stream.LocalPort
DeviceGEV.SetStreamDestination(LocalIP, np.uint16(LocalPort))
