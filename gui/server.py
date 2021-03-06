from threading import *
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from struct import *


class Signal(QObject):
    conn_signal = pyqtSignal()
    recv_signal = pyqtSignal(str, str, str, str)


class ServerSocket:

    def __init__(self, parent):
        self.parent = parent
        self.bListen = False
        self.clients = []
        self.ip = []
        self.threads = []

        self.conn = Signal()
        self.recv = Signal()

        self.conn.conn_signal.connect(self.parent.updateClient)
        self.recv.recv_signal.connect(self.parent.updateMsg)

    def __del__(self):
        self.stop()

    def start(self, ip, port):
        self.server = socket(AF_INET, SOCK_STREAM)

        try:
            self.server.bind((ip, port))
        except Exception as e:
            print('Bind Error : ', e)
            return False
        else:
            self.bListen = True
            self.t = Thread(target=self.listen, args=(self.server,))
            self.t.daemon = True
            self.t.start()
            print('Server Listening...')

        return True

    def stop(self):
        self.bListen = False
        if hasattr(self, 'server'):
            self.server.close()
            print('Server Stop')

    def listen(self, server):
        while self.bListen:
            server.listen(5)
            try:
                client, addr = server.accept()
            except Exception as e:
                print('Accept() Error : ', e)
                break
            else:
                self.clients.append(client)
                self.ip.append(addr)
                self.conn.conn_signal.emit()
                t = Thread(target=self.receive, args=(addr, client))
                t.daemon = True
                self.threads.append(t)
                t.start()

        self.removeAllClients()
        self.server.close()

    def receive(self, addr, client):
        while True:
            try:
                recv = client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                if recv:               
                    header = hex(recv[0])
                    cmd = hex(recv[1])
                    addr = hex((recv[2]<<8) | recv[3])
                    data = hex((recv[4]<<8) | recv[5])

                    self.recv.recv_signal.emit(header, cmd, addr, data)
                    # self.recv.recv_signal.emit(cmd)
                    # self.recv.recv_signal.emit(data)

        self.removeCleint(addr, client)

    def send(self, msg):
        try:
            for c in self.clients:
                c.send(msg)
        except Exception as e:
            print('Send() Error : ', e)

    def removeCleint(self, addr, client):
        client.close()
        self.ip.remove(addr)
        self.clients.remove(client)

        self.conn.conn_signal.emit()

        i = 0
        for t in self.threads[:]:
            if not t.isAlive():
                del (self.threads[i])
            i += 1

        self.resourceInfo()

    def removeAllClients(self):
        for c in self.clients:
            c.close()

        self.ip.clear()
        self.clients.clear()
        self.threads.clear()

        self.conn.conn_signal.emit()

        self.resourceInfo()

    def resourceInfo(self):
        print('Number of Client ip\t: ', len(self.ip))
        print('Number of Client socket\t: ', len(self.clients))
        print('Number of Client thread\t: ', len(self.threads))
