# import socket
import struct
from socket import *
from struct import *

# s = socket(AF_INET, SOCK_STREAM)
# addr = ('127.0.1.1', 5614)
# s.connect(addr)

# header
header = 0x41

# CMD
cmd = 0x02

# Data 
data = 0x003

values = (header, cmd, data)
fmt = '>B B H'
packer = struct.Struct(fmt)
sendData = packer.pack(*values)

# try:
#     s.sendall(sendData)
# finally:
#     s.close()

import socket

# 접속 정보 설정
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
SIZE = 1024
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

# 클라이언트 소켓 설정
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(SERVER_ADDR)  # 서버에 접속
    client_socket.send(sendData)  # 서버에 메시지 전송
    msg = client_socket.recv(SIZE)  # 서버로부터 응답받은 메시지 반환
    print("resp from server : {}".format(msg))  # 서버로부터 응답받은 메시지 출력