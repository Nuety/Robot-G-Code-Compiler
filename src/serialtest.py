import serial
import time


arduino = serial.Serial(port='/dev/cu.usbmodem1101',   baudrate=115200, timeout=.1)



def sendtoard(x):
    arduino.write(bytes(x, 'utf-8'))
    return

# sendtoard('1')


while (True):
    inp = input()
    arduino.write(bytes(inp, 'utf-8'))
    data = arduino.readline()
    print(data)

arduino.close()