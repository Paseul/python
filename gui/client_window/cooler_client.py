from multiprocessing import Process, Queue
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import struct
import datetime
import csv

class Signal(QObject):
    recv_signal = pyqtSignal(int, int, int)
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
        print(ip)

        try:
            self.client.connect((ip, port))
        except Exception as e:
            print('Connect Error : ', e)
            return False
        else:
            self.bConnect = True
            self.t = Process(target=self.receive, args=(self.client,))
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
        # basename = "cooler"
        # suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        # filename = "_".join([basename, suffix + ".csv"])
        # csvfile = open(filename, 'w', newline='')
        # writer = csv.writer(csvfile)
        try:
            while self.bConnect:
                try:
                    recv = client.recv(1024)
                except Exception as e:
                    print('Recv() Error :', e)
                    break
                else:
                    if recv:
                        if recv[7] == 5:
                            val1 = recv[4]<<8 | recv[5]
                            val2 = 0

                        elif recv[7] == 4:
                            val1 = recv[9]<<8 | recv[10]     # in temp
                            val2 = recv[11]<<8 | recv[12]     # out temp

                        elif recv[7] == 1:
                            val1 = recv[9]
                            val2 = 0

                        else:
                            val1 = 0
                            val2 = 0
                        print(val1, val2)
                        self.recv.recv_signal.emit(recv[7], val1, val2)
                        suffix = datetime.datetime.now().strftime("%H:%M:%S")
                        log_list = list(recv)
                        log_list.insert(0, suffix)
                        # writer.writerow(log_list)
                        print(recv)
            self.stop()
        except:
            pass

    def send(self, sendData):
        if not self.bConnect:
            return
        try:
            print(sendData)
            self.client.send(sendData)
        except Exception as e:
            print('Send() Error : ', e)