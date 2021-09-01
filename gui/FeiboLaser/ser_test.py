# sudo chmod 666 /dev/ttyUSB0
# ls -al /dev/ttyUSB*

import serial

port = '/dev/ttyUSB0' # 시리얼 포트
baud = 9600 # 시리얼 보드레이트(통신속도)
ser = serial.Serial(port, baud, timeout = 1)
line = []

while True:
    print("insert op :", end=' ')
    op = input()
    if op == 'q':
      ser.write('STATUS=123456789abcdef'.encode())

      
    for c in ser.readline():  
      #line 변수에 차곡차곡 추가하여 넣는다.      
      # print(chr(c))
      if chr(c) == '=':
        a = ''.join(line)
        line = []
        continue
      line.append(chr(c))
    s = ''.join(line) 
    # print(a)
    print(s)
    ser.write(op.encode())


