# sudo chmod 666 /dev/ttyUSB0
# sudo python serial.py
# ls -al /dev/ttyUSB*

 #-*- coding: utf-8 -*-
import serial
import time
import signal
import threading


line = [] #라인 단위로 데이터 가져올 리스트 변수

port = '/dev/ttyUSB0' # 시리얼 포트
baud = 115200 # 시리얼 보드레이트(통신속도)

exitThread = False   # 쓰레드 종료용 변수

#쓰레드 종료용 시그널 함수+
def handler(signum, frame):
     exitThread = True


#데이터 처리할 함수
def parsing_data(data):
    print(data)
    if data[0] == 2:
        print("header received")
        print(hex(data[3]), hex(data[4]))
        print(hex(data[3]<<8 | data[4]))
        # tmp = hex(int(data[3])) <<8 | hex(int(data[4]))
        # print(tmp)

    # 리스트 구조로 들어 왔기 때문에
    # 작업하기 편하게 스트링으로 합침
    # tmp = ''.join(data)

    # #출력!
    # print(tmp)

#본 쓰레드
def readThread(ser):
    global line
    global exitThread
    count = 0
    # 쓰레드 종료될때까지 계속 돌림
    while not exitThread:
        #데이터가 있있다면
        for c in ser.read():
            #line 변수에 차곡차곡 추가하여 넣는다.
            line.append(c)

            # print(hex(c))
            if len(line) == 20 and c == 3:  #라인의 끝을 만나면..
                #데이터 처리 함수로 호출
                parsing_data(line)

                #line 변수 초기화
                del line[:]                
                count += 1

                if count == 5:
                    exitThread = True

if __name__ == "__main__":
    #종료 시그널 등록
    signal.signal(signal.SIGINT, handler)

    #시리얼 열기
    ser = serial.Serial(port, baud, timeout=0)

    #시리얼 읽을 쓰레드 생성
    thread = threading.Thread(target=readThread, args=(ser,))

    #시작!
    thread.start()