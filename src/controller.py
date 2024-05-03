import gcodehandler as gch
import rtde_control
import rtde_receive
import re
import math
import serial

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

    def sendCommandToArduino(self, state):
        pass

    def returnHome(self):
        rtde_c.moveJ(homeJ, 2, 2)
                
    def setExtrusion(self, g):
        #set extrution mode
        if g == "G0":
            #stop printing if G0
            self.extruding = False
            arduino.write(bytes("G0", 'utf-8')) 
        elif g == "G1":
            #start printing if G1
            self.extruding = True
            arduino.write(bytes("G1", 'utf-8')) 
    
    def run(self, path):
        #the midpoint where the hotplate should sit is 0.46,0,0
        #tot is to calculate a simple percentage meter
        tot = len(path)
        height = 0.0
        speed = 0.015
        for i, segment in enumerate(path):
           #0, 1, 2, 3, 4, 5
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
                                    self.sendCommandToArduino(self.extruding)


                                rtde_c.moveL([0.46 + x, y, height+0.1, rotation[0], rotation[1], rotation[2]], speed, 4)
                                
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


            



ctrl = controller()
path = GCHandler.convertCode(commands)
ctrl.run(path)

