import socket
import struct
from socket import *
from struct import *

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 5000        # Port to listen on (non-privileged ports are > 1023)
SIZE = 1024
ADDR = (HOST, PORT)

# 서버 소켓 설정
with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind(ADDR)  # 주소 바인딩
    server_socket.listen()  # 클라이언트의 요청을 받을 준비

    # 무한루프 진입
    while True:
        client_socket, client_addr = server_socket.accept()  # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 반환
        msg = client_socket.recv(SIZE)  # 클라이언트가 보낸 메시지 반환
        msg = list(msg)
        a = hex(msg[0])
        b = hex(msg[1])
        x = (msg[2]<<8) | msg[3]
        c = hex(x)
        print("[{}] message : {} {} {}".format(client_addr, a, b, c))  # 클라이언트가 보낸 메시지 출력

        client_socket.sendall("welcome!".encode())  # 클라이언트에게 응답

        client_socket.close()  # 클라이언트 소켓 종료