from threading import *
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import struct


class Signal(QObject):
    recv_signal = pyqtSignal(int, int, int, int)
    disconn_signal = pyqtSignal()


class ClientSocket:

    def __init__(self, parent):
        self.parent = parent

        self.recv = Signal()
        self.recv.recv_signal.connect(self.parent.updateCooler)
        self.disconn = Signal()
        self.disconn.disconn_signal.connect(self.parent.coolerDisconnect)

        self.bConnect = False

    def __del__(self):
        self.stop()

    def connectServer(self, ip, port):
        self.client = socket(AF_INET, SOCK_STREAM)

        try:
            self.client.connect((ip, port))
        except Exception as e:
            print('Connect Error : ', e)
            return False
        else:
            self.bConnect = True
            self.t = Thread(target=self.receive, args=(self.client,))
            self.t.daemon = True
            self.t.start()
            print('Connected')

        return True

    def stop(self):
        self.bConnect = False
        if hasattr(self, 'client'):
            self.client.close()
            del (self.client)
            print('Client Stop')
            self.disconn.disconn_signal.emit()

    def receive(self, client):
        while self.bConnect:
            try:               
                recv = client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                if recv:                    
                    fmt = '>B B B B H H B'
                    unpacked = struct.unpack(fmt, recv)

                    self.recv.recv_signal.emit(unpacked[3], unpacked[4], unpacked[5], unpacked[6])
        self.stop()

    def send(self, sendData):
        if not self.bConnect:
            return
        try:
            self.client.send(sendData)
        except Exception as e:
            print('Send() Error : ', e)