from threading import *
from bluepy.btle import Scanner, DefaultDelegate
from PyQt5.QtCore import Qt, pyqtSignal, QObject

class Signal(QObject):
    recv_signal = pyqtSignal(float, float)

class DecodeErrorException(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            #print ("Discovered device", dev.addr)
            pass
        elif isNewData:
            #print ("Received new data from", dev.addr)
            pass

class ThermoBeacon:
    def __init__(self, parent):
        self.parent = parent
        
        self.recv = Signal()
        self.recv.recv_signal.connect(self.parent.thermoBeacon)  

        self.t = Thread(target=self.thermoBeacon)
        self.t.daemon = True
        self.t.start()

    def thermoBeacon(self):
        scanner = Scanner().withDelegate(ScanDelegate())
        try:
            while (True):
                devices = scanner.scan(1.0)

                ManuData = ""

                for dev in devices:
                    if dev.addr == "dc:12:00:00:06:a5":
                        CurrentDevAddr = dev.addr
                        for (adtype, desc, value) in dev.getScanData():
                            if (desc == "Manufacturer"):
                                ManuData = value

                        if (ManuData == ""):
                            print ("No data received, end decoding")
                            continue

                        
                        ManuDataHex = []
                        for i, j in zip (ManuData[::2], ManuData[1::2]):
                            ManuDataHex.append(int(i+j, 16))

                        if not len(ManuDataHex) == 20:
                            continue

                        tempidx = 12
                        humidityidx = 14

                        TempData = ManuDataHex[tempidx]
                        TempData += ManuDataHex[tempidx+1] * 0x100
                        TempData = TempData * 0.0625
                        if TempData > 4000:
                            TempData = -1 * (4096 - TempData)

                        HumidityData = ManuDataHex[humidityidx]
                        HumidityData += ManuDataHex[humidityidx+1] * 0x100
                        HumidityData = HumidityData * 0.0625

                        self.recv.recv_signal.emit(TempData, HumidityData)
            
        except DecodeErrorException:
            print("Decode Exception")
            pass
