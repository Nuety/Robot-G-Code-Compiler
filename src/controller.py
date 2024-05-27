import gcodehandler as gch
import rtde_control
import rtde_receive
import re
import math
import serial
import time

#it is very important this is calibrated before running the printer
heighoffset = 0.11532


#TODO save magic constants in seperate file

homeJ = [math.radians(13), math.radians(-120), math.radians(-103), math.radians(-45), math.radians(90), math.radians(103)]
rotation = [0, 3.14, 0]
homeL = [0.46, 0, 0.35, rotation[0], rotation[1], rotation[2]]
xoffset = -0.05
yoffset = 0.00

arduino = serial.Serial(port='/dev/cu.usbmodem1101',   baudrate=115200, timeout=.1)

#init robot connection
rtde_c = rtde_control.RTDEControlInterface("192.168.3.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.3.102")

GCHandler = gch.GCodeHandler()
commands = GCHandler.readfile("CE3PRO_bird_whistle.gcode")


class controller():
    def __init__(self) -> None:
        self.relative = False
        self.oldExtruding = False
        self.extruding = False

    def sendCommandToArduino(self, command):
        try:
            arduino.write(bytes(command, 'utf-8')) 
        except:
            print(f"Send Command failed {command}")

    def setTemperature(self, cmd, temp):
        self.sendCommandToArduino(" ".join([cmd, str(temp)]))


    #G28
    def returnHome(self):
        rtde_c.moveL(homeL, 1, 0.5)
                
    #enable or disable extrusion, used by G1 and G0 commands
    def setExtrusion(self, cmd):
        #set extrution mode
        self.extruding = cmd[1]
        self.sendCommandToArduino(cmd)

    
    def run(self, path):
        #the midpoint where the hotplate should sit is 0.46,0,0
        #tot is to calculate a simple percentage meter
        tot = len(path)
        height = 0.0
        speed = 0.015
        for i, segment in enumerate(path):
            #0, 1, 2, 3, 4, 5
            #TODO MAKE THIS BETTER DONT USE LENGTH
            print(segment)
            match len(segment):
                case 2:
                    cmd, s = segment
                case 6:
                    cmd, x, y, z, f, e = segment
            match cmd:
                #if it is either G0 or G1 make the move and 
                case "G0" | "G1":
                    print(f"{((i/tot)*100):.4f}% x: {x}, y: {y}, z: {height}")
                    #if height is set in the command change the command
                    

                    #if speed is set change speed
                    if f:
                        #speed in gcode is mm/min and robot moves in m/s so we divide by 60000
                        speed = f/60000

                    self.setExtrusion(cmd)
                        

                    match self.relative:
                        
                        # relative control had severe issues

                        # case True:
                        #     currentPos = rtde_r.getActualTCPPose()

                        #     #if xyz is None set to 0 to remove float addition error
                        #     x = 0 if not x else x
                        #     y = 0 if not y else y
                        #     z = 0 if not z else z

                        #     rtde_c.moveL([currentPos[0] + x, currentPos[1] + y, currentPos[2] + z, rotation[0], rotation[1], rotation[2]], speed, 0.5)
                            

                        case False:
                            if z:
                                height = z
                                
                            #move the robotarm if both x and y exist
                            if x and y:
                                # no need to oversend extrusion commands if the same command is the same as before.
                                if self.extruding != self.oldExtruding:
                                    self.sendCommandToArduino(cmd)


                                rtde_c.moveL([0.36 + x + xoffset, y + yoffset - 0.1, height+heighoffset, rotation[0], rotation[1], rotation[2]], speed, 0.5)
                                
                                # update the command.
                                self.oldExtruding = self.extruding
                case "G28":
                    self.returnHome()

                #Absolute Positioning
                case "G90":
                    self.relative = False
                    print("relative OFF")
                #Relative Positioning
                case "G91":
                    self.relative = True
                    print("relative ON")

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
    #when finished move to home
    rtde_c.moveL(homeL, 0.05, 0.5)

finally:
    ctrl.sendCommandToArduino("G0")
    ctrl.sendCommandToArduino("M104 30")
    ctrl.sendCommandToArduino("M109 30")

