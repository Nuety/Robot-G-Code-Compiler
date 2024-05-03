import serial 
import time 
arduino = serial.Serial(port='/dev/cu.usbmodem1101', baudrate=115200, timeout=.01) 

def write_read(x): 
    arduino.write(bytes(x, 'utf-8')) 
    data = arduino.readline() 
    return data 


while True: 
    num = input("Enter a command: ") # Taking input from user 
    value = write_read(num) 
    # time.sleep(0.01)
    print(value) # printing the value 
