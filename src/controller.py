import gcodehandler as gch
import rtde_control
import rtde_receive
import re
import math
import serial
import time


#TODO save magic constants in seperate file

homeJ = [math.radians(13), math.radians(-120), math.radians(-103), math.radians(-45), math.radians(90), math.radians(103)]
homeL = [0.46, 0, 0.5]
rotation = [0, 3.14, 0]

arduino = serial.Serial(port='/dev/cu.usbmodem1101',   baudrate=115200, timeout=.1)

#init robot connection
rtde_c = rtde_control.RTDEControlInterface("192.168.3.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.3.102")

GCHandler = gch.GCodeHandler()
commands = GCHandler.readfile("20mm_cube.gcode")


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

    def setTemperature(self, g, temp):
        self.sendCommandToArduino(" ".join([g, str(temp)]))


    #G28
    def returnHome(self):
        rtde_c.moveJ(homeJ, 2, 2)
                
    #enable or disable extrusion, used by G1 and G0 commands
    def setExtrusion(self, g):
        #set extrution mode
        self.extruding = g[1]
        self.sendCommandToArduino(g)
        #if self.extruding is not needed this can be shortened.
        # if g == "G0":
        #     #stop printing if G0
        #     self.extruding = False
        #     self.sendCommandToArduino(g)
        # elif g == "G1":
        #     #start printing if G1
        #     self.extruding = True
        #     self.sendCommandToArduino(g)

    
    def run(self, path):
        #the midpoint where the hotplate should sit is 0.46,0,0
        #tot is to calculate a simple percentage meter
        tot = len(path)
        height = 0.0
        speed = 0.015
        for i, segment in enumerate(path):
            #0, 1, 2, 3, 4, 5
            match len(segment):
                case 2:
                    g, s = segment
                case 6:
                    g, x, y, z, f, e = segment
            match g:
                #if it is either G0 or G1 make the move and 
                case "G0" | "G1":
                    print(f"{((i/tot)*100):.4f}% x: {x}, y: {y}, z: {height}")
                    #if height is set in the command change the command
                    if z:
                        height = z

                    #if speed is set change speed
                    if f:
                        #speed in gcode is mm/min and robot moves in m/s so we divide by 60000
                        speed = f/60000

                    self.setExtrusion(g)
                        

                    match self.relative:
                        case True:
                            pass

                        case False:
                            #move the robotarm if both x and y exist
                            if x and y:
                                # no need to oversend extrusion commands if the same command is the same as before.
                                if self.extruding != self.oldExtruding:
                                    self.sendCommandToArduino(g)


                                rtde_c.moveL([0.34 + x, y - 0.1, height+0.11265, rotation[0], rotation[1], rotation[2]], speed, 4)
                                
                                # update the command.
                                self.oldExtruding = self.extruding
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
finally:
    ctrl.sendCommandToArduino("G0")
    ctrl.sendCommandToArduino("M104 30")
    ctrl.sendCommandToArduino("M109 30")


