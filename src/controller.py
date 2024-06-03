import gcodehandler as gch
import rtde_control
import rtde_receive
import math
import serial

#It is very important this is calibrated before running the printer
#The number should be the average of the calibrated height
heightoffset = 0.11532
#Make sure that the head is always turning down, rx = 0, ry = pi, rz = 0
rotation = [0, 3.14, 0]
homeL = [0.46, 0, 0.35, rotation[0], rotation[1], rotation[2]]
#Extruder offset from arm
xoffset = -0.05
yoffset = 0.00

#Name of gcode file
filename = "yourmodel.gcode"

#Serial port should be the one used
arduino = serial.Serial(port='/dev/cu.usbmodem1101',   baudrate=115200, timeout=.1)

#Init robot connection
rtde_c = rtde_control.RTDEControlInterface("192.168.3.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.3.102")

GCHandler = gch.GCodeHandler()
commands = GCHandler.readfile(filename)


class controller():
    def __init__(self) -> None:
        self.relative = False
        self.oldExtruding = False
        self.extruding = False

    #Method for sending commands to the Arduino
    def sendCommandToArduino(self, command):
        try:
            arduino.write(bytes(command, 'utf-8')) 
        except:
            print(f"Send Command failed {command}")

    #Method for sending temperature specific commands to the Arduino
    def setTemperature(self, cmd, temp):
        self.sendCommandToArduino(" ".join([cmd, str(temp)]))


    #G28
    def returnHome(self):
        rtde_c.moveL(homeL, 1, 0.5)
                
    #Enable or disable extrusion, determined by G1 and G0 commands
    def setExtrusion(self, cmd):
        #Set extrution mode
        self.extruding = cmd[1]
        self.sendCommandToArduino(cmd)

    
    def run(self, path):
        #The midpoint where the hotplate should sit is 0.46,0,0
        #Tot is to calculate a simple percentage meter
        tot = len(path)
        height = 0.0
        speed = 0.015
        for i, segment in enumerate(path):
            #TODO MAKE THIS BETTER DONT USE LENGTH
            match len(segment):
                #If temperature
                case 2:
                    cmd, s = segment
                #If G1/0 command
                case 6:
                    cmd, x, y, z, f, e = segment
            match cmd:
                #If it is either G0 or G1 make the move and 
                case "G0" | "G1":
                    #Simple percentage of commands
                    print(f"{((i/tot)*100):.4f}% x: {x}, y: {y}, z: {height}")
                    #If speed is set change speed
                    if f:
                        #Speed in gcode is mm/min and robot moves in m/s so we divide by 60000
                        speed = f/60000
                    
                    self.setExtrusion(cmd)

                    if not self.relative:
                        if z:
                            height = z
                        #Move the robotarm if both x and y exist
                        if x and y:
                            #No need to oversend extrusion commands if the same command is the same as before.
                            if self.extruding != self.oldExtruding:
                                self.sendCommandToArduino(cmd)
                            rtde_c.moveL([0.36 + x + xoffset, y + yoffset - 0.1, height+heightoffset, rotation[0], rotation[1], rotation[2]], speed, 0.5)
                            #Update the command.
                            self.oldExtruding = self.extruding
                #Return home command
                case "G28":
                    self.returnHome()
                #Absolute Positioning
                case "G90":
                    self.relative = False
                #Relative Positioning
                case "G91":
                    self.relative = True
                #Set temperature of nozzle (non blocking)
                case "M104":
                    self.setTemperature("M104", s)
                #Set temperature of bed (non blocking)
                case "M140":
                    self.setTemperature("M140", s)
                #Set temperature of nozzle (blocking)
                case "M109":
                    self.setTemperature("M109", s)
                #Set temperature of bed (blocking)
                case "M190":
                    self.setTemperature("M190", s)
            

try:
    ctrl = controller()
    path = GCHandler.convertCode(commands)
    ctrl.run(path)
    #When finished move to home
    ctrl.returnHome()
#Stop extruding and cool components
finally:
    ctrl.sendCommandToArduino("G0")
    ctrl.sendCommandToArduino("M104 30")
    ctrl.sendCommandToArduino("M109 30")

